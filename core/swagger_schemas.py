from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema


class ManualParametersAutoSchema(SwaggerAutoSchema):
    def get_query_parameters(self):
        query_serializer = self.get_query_serializer()
        serializer_parameters = []
        if query_serializer is not None:
            serializer_parameters = self.serializer_to_parameters(query_serializer, in_=openapi.IN_QUERY)
        return serializer_parameters
