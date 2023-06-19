from rest_framework.views import APIView, Request, Response, status
from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsAccountOwner
from django.contrib.auth.hashers import make_password


class UserView(APIView):
    def post(self, request: Request) -> Response:
        """
        Registro de usuários
        """
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]

    def get(self, request: Request, pk: int) -> Response:
        """
        Obtenção de usuário
        """
        user = get_object_or_404(User, pk=pk)

        self.check_object_permissions(request, user)

        serializer = UserSerializer(user)

        return Response(serializer.data)

    def patch(self, request: Request, pk: int) -> Response:
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)

        password = request.data.get("password")
        if password:
            hashed_password = make_password(password)
            request.data["password"] = hashed_password

        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request: Request, pk: int) -> Response:
        """
        Deleção de usuário
        """
        user = get_object_or_404(User, pk=pk)

        self.check_object_permissions(request, user)

        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
