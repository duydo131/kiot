import pytz
import jwt
import inspect, os

from django.db.models import Model
from django.utils.deconstruct import deconstructible
from rest_framework import serializers
from rest_framework.authentication import (
    get_authorization_header,
)
from django.db import connection, reset_queries
import time
import functools

timezone = pytz.timezone('Asia/Ho_Chi_Minh')


def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print("Function : " + func.__name__)
        print("Number of Queries : {}".format(end_queries - start_queries))
        print("Finished in : {}".format(end - start))

        return result

    return inner_func


def localize_datetime(datetime):
    return timezone.localize(datetime)


def create_model(data, serializer_model):
    try:
        serializer = serializer_model(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        raise Exception("error")
        return serializer
    except Exception as e:
        pass


@deconstructible
class GenCacheKey:
    def __init__(self, request):
        payload_data = get_values_token(request)
        if payload_data is None:
            self.key_prefix = "Ftech_cache"
        else:
            self.key_prefix = 'User_' + str(payload_data['id']) + "_" + request.path


def get_values_token(request):
    auth = get_authorization_header(request).split()
    try:
        token = auth[1]
    except:
        return None
    payload_data = jwt.decode(token, verify=False)
    return payload_data


def invalidRating(value, field):
    if value < 1 or value > 10:
        raise serializers.ValidationError(f"{field} is not in [1, 10]".format(field=field))
    return value


def validate_positive(value, field):
    if value < 0:
        raise serializers.ValidationError(f"{field} must be positive".format(field=field))
    return value


def to_dict(model: Model, keys: list = None):
    if keys is None:
        keys = [field.name for field in model._meta.fields]
    return {key: getattr(model, key) for key in keys}
