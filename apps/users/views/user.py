from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from django.db.models import Count, Sum
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, exceptions
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.carts.serializers.cart import CartSerializer, CartReadOnlySerializer, CartAdditionalSerializer, \
    CartDeleteProductSerializer
from apps.users.filters import UserFilterSet
from apps.users.helper.user import get_user_by_params, get_total_product_by_users
from apps.users.models.user import User, UserRole
from apps.users.serializers import UserSerializer, UserReadOnlySerializer, LoginSerializer
from apps.users.serializers.user import RegisterSerializer, UserRegisterSerializer, UserListInputSerializer
from core.base_view import BaseView
from core.mixins import GetSerializerClassMixin
from core.permissions import IsUser, IsManager
from core.swagger_schemas import ManualParametersAutoSchema


class UserViewSet(GetSerializerClassMixin, viewsets.ModelViewSet, BaseView):
    permission_classes = []
    queryset = User.objects.all()
    queryset_detail = User.objects.filter()
    serializer_class = UserSerializer
    serializer_detail_class = UserReadOnlySerializer
    inp_serializer_cls = UserListInputSerializer

    serializer_action_classes = {
        "list": UserReadOnlySerializer,
        "retrieve": UserReadOnlySerializer,
    }
    filterset_class = UserFilterSet

    def get_queryset(self):
        queryset = self.queryset.all()
        queryset = queryset.exclude(role=UserRole.ADMIN)
        request_data = self.request_data
        queryset = get_user_by_params(queryset, request_data)
        queryset = queryset.annotate(total_terminal=Count('terminals')).order_by('-total_terminal')

        return queryset

    @swagger_auto_schema(
        operation_description="Get me",
        auto_schema=ManualParametersAutoSchema,
        responses={200: UserReadOnlySerializer},
    )
    @action(
        methods=["GET"],
        detail=False,
        url_path="me",
        url_name="me",
        permission_classes=[IsAuthenticated],
        filterset_class=None,
        pagination_class=None,
    )
    def me(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_action_classes.get("retrieve")(
            user
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        users = queryset.filter()
        user_id_to_total_product = get_total_product_by_users(users)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(
                page,
                many=True,
                context={'user_id_to_total_product': user_id_to_total_product}
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
                queryset,
                many=True,
                context={'user_id_to_total_product': user_id_to_total_product}
        )
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Login",
        request_body=LoginSerializer,
        auto_schema=ManualParametersAutoSchema,
        responses={200: UserReadOnlySerializer},
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="login",
        url_name="login",
        filterset_class=None,
        permission_classes=[],
        pagination_class=None,
    )
    def login(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        try:
            user = authenticate(username=username, password=password)
        except exceptions.NotFound:
            raise APIException(
                _("User or password is wrong"),
                status.HTTP_404_NOT_FOUND,
            )
        except:
            raise APIException(_("Invalid token"), status.HTTP_400_BAD_REQUEST)
        if not user:
            raise APIException(
                _("User with username {username} not found").format(username=username),
                status.HTTP_404_NOT_FOUND,
            )
        token = user.token
        data = {"token": token, "is_superuser": user.is_superuser}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=False,
        url_path="register",
        url_name="register",
        filterset_class=None,
        permission_classes=[],
        pagination_class=None,
    )
    def register(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        try:
            with transaction.atomic():
                serializer = UserRegisterSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                user = dict(serializer.data)
                new_user = User.objects.get(id=user['id'])
                new_user.set_password(validated_data['password'])
                new_user.save()

                if new_user.is_user:
                    serializer = CartSerializer(data={
                        'user': new_user.id,
                    })
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
        except Exception as e:
            raise APIException(_("Cannot register user"), status.HTTP_500_INTERNAL_SERVER_ERROR)

        token = new_user.token
        data = {"token": token}
        return Response(data=data, status=status.HTTP_200_OK)

    # @swagger_auto_schema(
    #     operation_description="Get cart",
    #     auto_schema=ManualParametersAutoSchema,
    #     responses={200: CartReadOnlySerializer},
    # )
    @action(
        methods=["GET"],
        detail=False,
        url_path="cart",
        url_name="get_cart",
        permission_classes=[IsUser],
        filterset_class=None,
        pagination_class=None,
    )
    def get_cart(self, request, *args, **kwargs):
        user = request.user
        serializer = CartReadOnlySerializer(user.cart)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    #
    # @swagger_auto_schema(
    #     operation_description="Get cart",
    #     auto_schema=CartAdditionalSerializer,
    #     responses={200: CartReadOnlySerializer},
    # )

    @action(
        methods=["POST"],
        detail=False,
        url_path="update_cart",
        url_name="update_cart",
        permission_classes=[IsUser],
        filterset_class=None,
        pagination_class=None,
    )
    def update_cart(self, request, *args, **kwargs):
        user = request.user
        serializer = CartAdditionalSerializer(data=request.data, context={'cart': user.cart})
        serializer.is_valid(raise_exception=True)
        cart = serializer.save()
        return Response(data=CartReadOnlySerializer(cart).data, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=False,
        url_path="delete_product",
        url_name="delete_product",
        permission_classes=[IsUser],
        filterset_class=None,
        pagination_class=None,
    )
    def delete_product(self, request, *args, **kwargs):
        user = request.user
        serializer = CartDeleteProductSerializer(data=request.data, context={'cart': user.cart})
        serializer.is_valid(raise_exception=True)
        cart = serializer.save()
        return Response(data=CartReadOnlySerializer(cart).data, status=status.HTTP_200_OK)
