from calendar import monthrange
from numbers import Number

import pytz
import jwt
import datetime
import dateutil.relativedelta

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


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def validate_positive(value, field):
    if value < 0:
        raise serializers.ValidationError(f"{field} must be positive".format(field=field))
    return value


def to_dict(model: Model, keys: list = None):
    if keys is None:
        keys = [field.name for field in model._meta.fields]
    return {key: getattr(model, key) for key in keys}


def is_dict_values_none(row_data: dict):
    return all(x is None for x in row_data.values())


def iterate_all(iterable, ignore_keys=None, returned="key"):
    """Returns an iterator that returns all keys or values
       of a (nested) iterable.

       Arguments:
           - iterable: <list> or <dictionary>
           - returned: <string> "key" or "value"

       Returns:
           - <iterator>
    """

    if ignore_keys is None:
        ignore_keys = []
    if isinstance(iterable, dict):
        for key, value in iterable.items():
            if returned == "key":
                yield key
            elif returned == "value":
                if not (isinstance(value, dict) or isinstance(value, list)) and key not in ignore_keys:
                    yield value
            else:
                raise ValueError("'returned' keyword only accepts 'key' or 'value'.")
            for ret in iterate_all(value, returned=returned, ignore_keys=ignore_keys):
                yield ret
    elif isinstance(iterable, list):
        for el in iterable:
            for ret in iterate_all(el, returned=returned, ignore_keys=ignore_keys):
                yield ret


def get_any_day_ago(days: float):
    tod = datetime.datetime.now()
    d = datetime.timedelta(days=days)
    start_date = tod - d
    return start_date.strftime("%Y-%m-%d")


def get_date_any_day_ago(days: float):
    tod = datetime.datetime.now()
    d = datetime.timedelta(days=days)
    return tod - d


def get_any_month_ago(months: int):
    today = datetime.datetime.now()
    day_of_month = today + dateutil.relativedelta.relativedelta(months=1-months)
    start = day_of_month.date().replace(day=1)
    end = today.date().replace(day=monthrange(today.year, today.month)[1])

    return start, end

