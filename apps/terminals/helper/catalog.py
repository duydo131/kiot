
def get_by_catalog_import_input(queryset, request_data):
    ids = request_data.get('ids')
    if ids:
        queryset = queryset.filter(id__in=ids)

    started_at_from = request_data.get('started_at_from')
    if started_at_from is not None:
        queryset.filter(created_at__gte=started_at_from)

    ended_at_to = request_data.get('ended_at_to')
    if ended_at_to is not None:
        queryset.filter(created_at__lte=ended_at_to)

    user_id = request_data.get('user_id')
    if user_id is not None:
        queryset.filter(user_id=user_id)

    status = request_data.get('status')
    if status is not None:
        queryset.filter(status=status)

    return queryset
