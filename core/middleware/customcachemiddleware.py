from django.middleware.cache import UpdateCacheMiddleware

from core.task import update_cache


def remove_id(path):
    i = len(path)
    for i in reversed(range(len(path))):
        if path[i] == '/':
            break
    return path[0:i]


class RemoveCacheByPathMiddleware(UpdateCacheMiddleware):
    def process_response(self, request, response):
        if response.streaming or response.status_code not in (200, 304, 201):
            return response

        if request.method not in ('GET', 'HEAD'):
            path = request.path
            if request.method in ('PATCH', 'PUT'):
                path = remove_id(path)
            update_cache.apply_async(args=(path,))

        return response
