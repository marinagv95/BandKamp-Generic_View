from rest_framework.views import Request, Response, status


class CreateModelMixin:
    queryset = None
    serializer_class = None

    def create(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)
