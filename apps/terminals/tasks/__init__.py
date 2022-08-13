import datetime
import logging

import dateutil.utils

from apps.orders.models import Order
from apps.orders.models.order import OrderType
from apps.terminals.models import Terminal
from apps.terminals.models.terminal import TerminalStatus
from config import celery_app
from core.utils import get_date_any_day_ago

logger = logging.getLogger(__name__)


@celery_app.task()
def process_remove_new_terminal_fail():
    logger.info("start remove terminal register fail")
    one_week_ago = get_date_any_day_ago(7)
    Terminal.objects.filter(type__in=[TerminalStatus.FAIL, TerminalStatus.REGISTER, TerminalStatus.UNKNOWN], updated_at__lt=one_week_ago).delete()


@celery_app.task()
def process_restore_when_extend_terminal_fail():
    logger.info("start change type when extend terminal fail")
    one_week_ago = get_date_any_day_ago(7)
    Terminal.objects.filter(type__in=[TerminalStatus.EXTEND_FAIL, TerminalStatus.EXTEND], updated_at__lt=one_week_ago) \
        .update(
        type=TerminalStatus.PAID,
        extend_max_quantity_product=0,
        extend_time_selling=0
    )


@celery_app.task()
def process_open_sell_in_terminal():
    logger.info("start open sell in terminal")
    now = datetime.datetime.now()
    Terminal.objects.filter(type__in=[TerminalStatus.PAID, TerminalStatus.EXTEND_FAIL])\
        .filter(time_open__lte=now, expired_at__gte=now)\
        .update(status=True)


@celery_app.task()
def process_close_sell_in_terminal():
    logger.info("start close sell in terminal")
    now = datetime.datetime.now()
    Terminal.objects.filter(type__in=[TerminalStatus.PAID, TerminalStatus.EXTEND_FAIL])\
        .filter(expired_at__lte=now)\
        .update(status=False)


@celery_app.task()
def process_remove_order_not_success():
    logger.info("start remove order not success")
    one_week_ago = get_date_any_day_ago(7)
    Order.objects.filter(updated_at__lt=one_week_ago).exclude(type=OrderType.PAID).delete()
