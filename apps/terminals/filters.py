import django_filters
import datetime
from django.db.models import Q


class RoomFilterSet(django_filters.FilterSet):
    hotel = django_filters.CharFilter(lookup_expr="exact", field_name="hotel_id")
    day = django_filters.DateFromToRangeFilter(method="start_end_date")
    price = django_filters.RangeFilter(method="price_range")

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        return qs.distinct()

    def start_end_date(self, queryset, name, value):
        d2 = value.start
        d1 = value.stop
        if d1 >= d2:
            raise Exception("Date Error")

        query = Q(details__rent__start_date__gte=d1) | Q(details__rent__end_date__lte=d2) | \
                Q(details__rent__end_date__isnull=True)
        return queryset.filter(query)

    def price_range(self, queryset, name, value):
        d2 = value.start
        d1 = value.stop
        query = Q()
        if d1 and d2 and d1 < d2:
            raise Exception("Price Error")

        if d1:
            query &= Q(price__lte=d1)

        if d2:
            query &= Q(price__gte=d2)

        return queryset.filter(query)


class RoomCategoryFilterSet(django_filters.FilterSet):
    pass


class ServiceFilterSet(django_filters.FilterSet):
    room = django_filters.CharFilter(lookup_expr="exact", field_name="rooms__id")


class DeviceFilterSet(django_filters.FilterSet):
    room = django_filters.CharFilter(lookup_expr="exact", field_name="room_device__room__id")

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        return qs.distinct()


class RoomDeviceFilterSet(django_filters.FilterSet):
    room = django_filters.CharFilter(lookup_expr="exact", field_name="room__id")

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        return qs.distinct()