import logging
from django.http.response import Http404
from django.core.exceptions import PermissionDenied
from rest_framework.views import exception_handler, set_rollback
from rest_framework import exceptions
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.response import Response

logger = logging.getLogger(__name__)


def get_full_name(obj):
    """
    Helper function to get fully qualified class name of an object
    """
    # o.__module__ + "." + o.__class__.__qualname__ is an example in
    # this context of H.L. Mencken's "neat, plausible, and wrong."
    # Python makes no guarantees as to whether the __module__ special
    # attribute is defined, so we take a more circumspect approach.
    # Alas, the module name is explicitly excluded from __qualname__
    # in Python 3.

    module = obj.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return obj.__class__.__name__  # Avoid reporting __builtin__
    else:
        return module + '.' + obj.__class__.__name__


def custom_exception_handler(exc, context):
    """
    There are basically 2 type of exceptions when using Django Rest Framework:
    - APIException and derivatives
    - Generic exceptions: from django and system
    """
    errors = []
    headers = {}

    if isinstance(exc, APIException):

        # --- copy from exception_handler ---
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait
        # --- end copy ---

        if isinstance(exc, ValidationError):
            """
            exc.detail format:
            {
                <field_name> : [ List of ErrorDetail ]
            }
            """
            def add_error_detail(err_detail, parent_field=None):
                for field, validation_errors in err_detail.items():
                    for validation_error in validation_errors:
                        _parent_field = f"{parent_field}." if parent_field else ""
                        if isinstance(validation_error, dict):
                            add_error_detail(validation_error,
                                             f"{_parent_field}{field}")
                        else:
                            try:
                                errors.append({
                                    "field": f"{_parent_field}{field}",
                                    "code": f"{validation_error.code}",
                                    "message": str(validation_error)
                                })
                            except:
                                for error in err_detail[field]:
                                    errors.append({
                                        "field": f"{_parent_field}{field}",
                                        "code": f"{error.code}",
                                        "message": str(error)
                                    })

            if isinstance(exc.detail, dict):
                add_error_detail(exc.detail)
            elif isinstance(exc.detail, list):
                for err_detail in exc.detail:
                    add_error_detail(err_detail)
        else:  # Maybe one of 2 types: list or dict
            if isinstance(exc.detail, list):
                logger.exception(exc)  # TODO: log for further expandsion
            elif isinstance(exc.detail, dict):
                logger.exception(exc)  # TODO: log for further expandsion
            else:
                errors.append({
                    "code": exc.detail.code,
                    "message": str(exc.detail),
                })

        set_rollback()
    else:
        if isinstance(exc, Http404):
            exc = exceptions.NotFound()
        elif isinstance(exc, PermissionDenied):
            exc = exceptions.PermissionDenied()
        else:
            logger.exception(exc)

        errors.append({
            "code": get_full_name(exc),
            "message": str(exc)
            or get_full_name(exc)  # In case str(exc) return empty string
        })

    return Response(
        {"errors": errors},
        status=exc.status_code if hasattr(exc, 'status_code') else 500,
        headers=headers,
    )
