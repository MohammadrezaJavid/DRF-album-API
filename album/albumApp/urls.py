from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'albums', viewset=views.AlbumViewSet, basename='album')
# router.register(r'users', viewset=views.UserViewSet, basename='user')

urlpatterns = [
    # path('albums/', views.AlbumViewSet.as_view({'get': 'list', 'post': 'create'}), name='album-list'),
    # path('albums/<int:id>/', views.AlbumViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
    #      name='album-detail'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls')),
]
