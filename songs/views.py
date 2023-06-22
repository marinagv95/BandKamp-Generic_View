from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Song
from rest_framework.pagination import PageNumberPagination
from .serializers import SongSerializer
from albums.models import Album
from rest_framework.generics import ListCreateAPIView


class SongView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = SongSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Song.objects.filter(album_id=pk)

    def perform_create(self, serializer):
        pk = self.kwargs["pk"]
        album = get_object_or_404(Album, pk=pk)
        serializer.save(album=album)
