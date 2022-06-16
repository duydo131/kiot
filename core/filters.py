import django_filters
from django_filters.filters import UUIDFilter
from django_filters.constants import EMPTY_VALUES
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import Lower


class UUIDInFilter(django_filters.BaseInFilter, UUIDFilter):
    pass


class CaseInsensitiveOrderingFilter(django_filters.OrderingFilter):
    def __init__(self, *args, **kwargs):
        self.case_insensitive_fields = kwargs.pop('case_insensitive_fields',
                                                  [])
        super().__init__(*args, **kwargs)

    def get_ordering_value(self, param):
        descending = param.startswith('-')
        param = param[1:] if descending else param
        field_name = self.param_map.get(param, param)
        return field_name, descending

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        ordering_fields = []
        for param in value:
            ordering_value, descending = self.get_ordering_value(param)
            if ordering_value in self.case_insensitive_fields:
                if descending:
                    ordering_fields.append(Lower(ordering_value).desc())
                else:
                    ordering_fields.append(Lower(ordering_value))
            else:
                if descending:
                    ordering_fields.append(f"-{ordering_value}")
                else:
                    ordering_fields.append(ordering_value)
        return qs.order_by(*ordering_fields)