from rest_framework_extensions.mixins import DetailSerializerMixin


class GetSerializerClassMixin:
    serializer_action_classes = {}
    serializer_detail_class = None
    queryset_detail = None

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            error_message = "'{0}' should include a 'serializer_detail_class' attribute".format(self.__class__.__name__)
            # assert self.serializer_detail_class is not None, error_message
            # if getattr(self, 'object', None):
            #     return self.serializer_detail_class
            # else:
            return super(GetSerializerClassMixin, self).get_serializer_class()

    def get_queryset(self):
        if self.action in ["update", "partial_update", "retrieve"]:
            return self.queryset_detail
        return self.queryset
