from rest_framework.views import Request, Response, APIView
from utilis.mixin import CreateModelMixin


class GenericAPIView(APIView):
    queryset = None
    serializer_class: None


class CreateAPIView(GenericAPIView, CreateModelMixin):
    def post(self, request: Request) -> Response:
        return super().create(request)
