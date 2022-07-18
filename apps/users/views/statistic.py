from django.db import connection
from django.db.models import Q, Sum, F
from django.db.models.functions import Coalesce
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.terminals.models import Terminal
from apps.terminals.serializers.statistic import StatisticProductSerializer, StatisticProductRequestSerializer
from apps.users.filters import UserFilterSet
from apps.users.models.user import User
from apps.users.serializers import UserSerializer, UserReadOnlySerializer
from core.mixins import GetSerializerClassMixin
from core.swagger_schemas import ManualParametersAutoSchema
from core.utils import dictfetchall


class StatisticViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    permission_classes = []
    queryset = User.objects.all()
    queryset_detail = User.objects.filter()
    serializer_class = UserSerializer
    serializer_detail_class = UserReadOnlySerializer

    http_method_names = ['get']

    serializer_action_classes = {
        "list": UserReadOnlySerializer,
        "retrieve": UserReadOnlySerializer,
    }
    filterset_class = UserFilterSet

    def get_queryset(self):
        queryset = self.queryset.all()
        return queryset

    @swagger_auto_schema(
        operation_description="get income",
        auto_schema=ManualParametersAutoSchema,
        responses={200: UserReadOnlySerializer},
    )
    @action(
        methods=["GET"],
        detail=False,
        url_path="income",
        url_name="income",
        permission_classes=[IsAuthenticated],
        filterset_class=None,
        pagination_class=None,
    )
    def income(self, request, *args, **kwargs):
        serializer = StatisticProductRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        user = request.user
        data = serializer.validated_data

        is_started_at_from = bool(data.get('started_at_from', None))
        is_ended_at_to = bool(data.get('ended_at_to', None))

        query = f"""
        with revenue_terminal as (
            SELECT 
                `terminals`.`id`, 
                COALESCE(SUM( CASE
                 WHEN (
                    true
                    { " AND `order_detail`.`created_at` >= %s" if is_started_at_from else '' }
                    { " AND `order_detail`.`created_at` <= %s" if is_ended_at_to else '' }
                    )
                     THEN (`order_detail`.`quantity` * `order_detail`.`sell_price`)
                 ELSE NULL END), 0) AS `revenue`
            FROM `terminals`
                     LEFT OUTER JOIN `product` ON (`terminals`.`id` = `product`.`terminal_id`)
                     LEFT OUTER JOIN `order_detail` ON (`product`.`id` = `order_detail`.`product_id`)
            WHERE (`terminals`.`deleted` IS NULL)
            GROUP BY `terminals`.`id`
        ), cost_terminal as (
            SELECT 
                `terminals`.`id`, 
                COALESCE(SUM( CASE
                WHEN (
                     true
                     { " AND `terminal_payment`.`created_at` >= %s " if is_started_at_from else '' }
                     { " AND `terminal_payment`.`created_at` <= %s" if is_ended_at_to else '' }
                     )
                     THEN `transactions`.`amount`
                ELSE NULL END), 0) AS `cost`
            FROM `terminals`
                 LEFT OUTER JOIN `terminal_payment` ON (`terminals`.`id` = `terminal_payment`.`terminal_id`)
                 LEFT OUTER JOIN `transactions` ON (`terminal_payment`.`transaction_id` = `transactions`.`id`)
            WHERE (`terminals`.`deleted` IS NULL)
            GROUP BY `terminals`.`id`
        ) 
        select 
            `terminals`.id as id,
            `terminals`.code as code,
            `terminals`.name as name,
            `revenue_terminal`.revenue as revenue,
            `cost_terminal`.cost as cost
        from `terminals`
        left join `revenue_terminal` on `terminals`.id = `revenue_terminal`.id
        left join `cost_terminal` on `terminals`.id = `cost_terminal`.id
        WHERE (
            true
            {" AND `terminals`.`seller_id` = %s " if user.is_manager else ''}
            {" AND `terminals`.`id` IN %s " if data.get('ids', None) else ''}
            AND `terminals`.`deleted` IS NULL
        )
        ORDER BY `revenue` DESC
        { f" LIMIT {data.get('limit')} " if data.get('limit', None) else ''}
        """

        params = []
        if is_started_at_from:
            params.append(data.get('started_at_from'))
        if is_ended_at_to:
            params.append(data.get('ended_at_to'))

        params.extend(params)
        if user.is_manager:
            params.append(user.id.hex)

        if data.get('ids', None):
            params.append(data.get('ids'))

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            terminals = dictfetchall(cursor)
        result = StatisticProductSerializer(terminals, many=True)
        return Response(data=result.data, status=status.HTTP_200_OK)
