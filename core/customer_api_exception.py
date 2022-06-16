from rest_framework import exceptions
from rest_framework import status
from django.utils.translation import gettext_lazy as _


class CustomerApiException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid input.')
    default_code = 'invalid'

    def __init__(self, detail=None, code=None, status_code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code
        if status_code:
            self.status_code = status_code

        self.detail = exceptions._get_error_details(detail, code)
