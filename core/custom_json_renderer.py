from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):

        if isinstance(data, dict):
            # check if `errors` in data
            # WARNING: depends on custom error handler
            if 'errors' in data:
                return super().render(data, accepted_media_type,
                                      renderer_context)
        return super().render({'data': data}, accepted_media_type,
                              renderer_context)

        # # if data is a list, we can sure that query was success
        # if isinstance(data, list):
        #     return super().render({'data': data}, accepted_media_type,
        #                           renderer_context)

        # if isinstance(data, dict):
        #     # check if `errors` in data
        #     # WARNING: depends on custom error handler
        #     if 'errors' in data:
        #         return super().render(data, accepted_media_type,
        #                               renderer_context)
        #     else:  # Wrap returned data in `data` field
        #         return super().render({'data': data}, accepted_media_type,
        #                               renderer_context)

        # # Default behaviour, considering it an error
        # return super().render(
        #     {'errors': [{
        #         'code': 'unknown',
        #         'message': data
        #     }]}, accepted_media_type, renderer_context)
