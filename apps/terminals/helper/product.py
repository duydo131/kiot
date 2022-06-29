from apps.terminals.models import Product


def get_by_product_input(queryset, request_data):
    ids = request_data.get('ids')
    if ids:
        queryset = queryset.filter(id__in=ids)

    name = request_data.get('name')
    if name is not None:
        queryset = queryset.filter(name__icontains=name)

    code = request_data.get('code')
    if code is not None:
        queryset = queryset.filter(code=code)

    sku = request_data.get('sku')
    if sku is not None:
        queryset = queryset.filter(sku=sku)

    terminal_id = request_data.get('terminal_id')
    if terminal_id is not None:
        queryset = queryset.filter(terminal_id=terminal_id)

    started_at_from = request_data.get('started_at_from')
    if started_at_from is not None:
        queryset = queryset.filter(created_at__gte=started_at_from)

    ended_at_to = request_data.get('ended_at_to')
    if ended_at_to is not None:
        queryset = queryset.filter(created_at__lte=ended_at_to)

    min_price = request_data.get('min_price')
    if min_price is not None:
        queryset = queryset.filter(price__gte=min_price)

    max_price = request_data.get('max_price')
    if max_price is not None:
        queryset = queryset.filter(price__gte=max_price)

    return queryset


def generate_code_for_product(sku, terminal_code, count=None):
    if count is None:
        count = Product.objects.count()
    return f"{terminal_code}__{sku}__{count}"


def generate_code_for_products(products):
    pass
