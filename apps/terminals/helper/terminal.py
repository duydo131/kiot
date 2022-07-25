from apps.terminals.models import Terminal
from config.settings.dev import PRICE_REGISTER_TERMINAL, PRICE_PER_DAY, PRICE_PER_BLOCK_PRODUCT, BLOCK_DAY, \
    BLOCK_QUANTITY_PRODUCT, IGNORE_DAY, IGNORE_QUANTITY_PRODUCT, PRICE_EXTEND_TERMINAL
from core.utils import timezone


def get_by_terminal_input(queryset, request_data, seller_id=None):
    if seller_id is not None:
        queryset = queryset.filter(seller_id=seller_id)

    ids = request_data.get('ids')
    if ids:
        queryset = queryset.filter(id__in=ids)

    name = request_data.get('name')
    if name:
        queryset = queryset.filter(name__icontains=name)

    code = request_data.get('code')
    if code:
        queryset = queryset.filter(code__icontains=code)

    is_expired = request_data.get('is_expired')
    if is_expired is not None:
        now = timezone.now()
        queryset = queryset.filter(expried_at__gte=now)

    status = request_data.get('status')
    if status is not None:
        queryset = queryset.filter(status=status)

    return queryset


def calculate_price_register_terminal(terminal: Terminal):
    max_quantity_product = terminal.max_quantity_product
    time_selling = terminal.time_selling

    quantity_product_calculate_price = max_quantity_product - IGNORE_QUANTITY_PRODUCT if max_quantity_product - IGNORE_QUANTITY_PRODUCT > 0 else 0
    price_of_product = quantity_product_calculate_price // BLOCK_QUANTITY_PRODUCT * PRICE_PER_BLOCK_PRODUCT

    quantity_day_calculate_price = time_selling - IGNORE_DAY if time_selling - IGNORE_DAY > 0 else 0
    price_of_day = quantity_day_calculate_price // BLOCK_DAY * PRICE_PER_DAY

    total_price = PRICE_REGISTER_TERMINAL + price_of_product + price_of_day
    return total_price


def calculate_price_extend_terminal(terminal: Terminal):
    price_of_product = 0
    price_of_day = 0

    if terminal.extend_max_quantity_product > 0:
        quantity_product_calculate_price = terminal.extend_max_quantity_product - terminal.max_quantity_product
        price_of_product = quantity_product_calculate_price // BLOCK_QUANTITY_PRODUCT * PRICE_PER_BLOCK_PRODUCT

    if terminal.extend_time_selling > 0:
        quantity_day_calculate_price = terminal.extend_time_selling
        price_of_day = quantity_day_calculate_price // BLOCK_DAY * PRICE_PER_DAY

    total_price = PRICE_EXTEND_TERMINAL + price_of_product + price_of_day
    return total_price
