from typing import List

from django.db.models import Count
from django.db.models.functions import Coalesce

from apps.users.models import User


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
