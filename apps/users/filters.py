import django_filters

from apps.users.models.user import UserGender
from core.filters import CaseInsensitiveOrderingFilter


class UserFilterSet(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains",
                                     field_name="name")
    fid = django_filters.CharFilter(field_name="fid")
    phone = django_filters.CharFilter(lookup_expr="icontains",
                                      field_name="phone")
    email = django_filters.CharFilter(lookup_expr="icontains",
                                      field_name="email")
    gender = django_filters.MultipleChoiceFilter(field_name="gender",
                                                 choices=UserGender.choices)
    ordering = django_filters.OrderingFilter(fields=("created_at",
                                                     "updated_at", "name"))


class StaffFilterSet(django_filters.FilterSet):
    channel = django_filters.UUIDFilter(field_name="channel_id")
    user = django_filters.UUIDFilter(field_name="user_id")
    roles = django_filters.CharFilter(field_name="roles",
                                      method="role_ids_filter")
    name = django_filters.CharFilter(lookup_expr="icontains",
                                     field_name="name")
    phone = django_filters.CharFilter(lookup_expr="icontains",
                                      field_name="phone")
    email = django_filters.CharFilter(lookup_expr="icontains",
                                      field_name="email")
    gender = django_filters.MultipleChoiceFilter(field_name="gender",
                                                 choices=UserGender.choices)
    ordering = CaseInsensitiveOrderingFilter(
        fields=("created_at", "updated_at", "name"),
        case_insensitive_fields=["name"],
    )

    def role_ids_filter(self, queryset, name, value):
        ids = value.split(",")
        return queryset.filter(role__id__in=ids)


class RoleFilterSet(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name")


class InviteUrlFilterSet(django_filters.FilterSet):
    creator = django_filters.UUIDFilter(field_name="creator_id")
    role_ids = django_filters.CharFilter(field_name="role_ids",
                                         method="role_ids_filter")

    def role_ids_filter(self, queryset, name, value):
        ids = value.split(",")
        return queryset.filter(role__id__in=ids)
