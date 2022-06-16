"""
    This module contains base classes and functions for PPM API
"""
import logging
from typing import Union

from rest_framework import serializers
from rest_framework.views import APIView

logger = logging.getLogger('main')


class BaseView(APIView):
    """
    Base class for all PPM API v1
    """
    # API template attributes
    inp_serializer_cls = None  # type: Union[serializers.Serializer, dict, None]
    out_serializer_cls = None  # type: Union[serializers.Serializer, dict, None]
    perms = None  # type: Union[serializers.Serializer, dict, None]
    __validated_data = None  # type: Union[dict, None]
    __request_data = None  # type: Union[dict, None]
    pagination_class = None

    @property
    def request_data(self):
        """get request data"""
        request_data = None
        if self.inp_serializer_cls:
            serializer = self.inp_serializer_cls(  # pylint: disable=E1102
                data={key: value for key, value in self.request.GET.dict().items() if value})  # type: ignore
            serializer.is_valid(raise_exception=True)
            request_data = serializer.validated_data
        return request_data

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        return self.pagination.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data, result_key='results'):
        """
        Return a paginated style `Response` object for the given output data.
        """
        return self.pagination.get_paginated_response(data, result_key=result_key)
