from rest_framework import viewsets, generics
from .models import Album
from .serializers import AlbumSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly


# User List
class UserList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer


# User Retrieve / Update / Destroy
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer


# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AlbumViewSet(viewsets.ModelViewSet):
    # lookup_field = 'pk'
    queryset = Album.objects.all().order_by('id')
    serializer_class = AlbumSerializer

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    ordering_fields = ['created']

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
