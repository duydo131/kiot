from typing import List, Dict

from django.db.models import Count, Sum, Q
from django.db.models.functions import Coalesce

from apps.users.models import User
from core.utils import get_any_month_ago


def get_user_by_params(queryset, request_data):
    ids = request_data.get('ids')
    if ids:
        queryset = queryset.filter(id__in=ids)

    role = request_data.get('role')
    if role:
        queryset = queryset.filter(role=role)

    return queryset


def get_total_product_by_users(users: List[User]):
    user_ids = [user.id for user in users]
    add_on_users = User.objects.filter(id__in=user_ids).annotate(total_product=Coalesce(Count('terminals__products'), 0))
    return {
        user.id: user.total_product
        for user in add_on_users
    }


def get_total_money_by_users(users: List[User], data=None):
    if data is None:
        data = {}
    user_ids = [user.id for user in users]
    condition = Q(id__in=user_ids)
    if data.get('type') == 'month':
        month = data.get('value', 1)
        start, end = get_any_month_ago(month)
        condition &= Q(transaction_set__created_at__range=[start, end])
    add_on_users = User.objects.filter(condition).annotate(total_money=Coalesce(Sum('transaction_set__amount'), 0))
    return {
        user.id: user.total_money
        for user in add_on_users
    }


def get_total_order_by_users(users: List[User], data=None):
    if data is None:
        data = {}
    user_ids = [user.id for user in users]
    condition = Q(id__in=user_ids)
    if data.get('type') == 'month':
        month = data.get('value', 1)
        start, end = get_any_month_ago(month)
        condition &= Q(orders__created_at__range=[start, end])
    add_on_users = User.objects.filter(condition).annotate(total_order=Coalesce(Count('orders'), 0))
    return {
        user.id: user.total_order
        for user in add_on_users
    }
