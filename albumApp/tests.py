import string

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from .serializers import UserSerializer
from .models import Album


class TestListAlbum(APITestCase):
    def setUp(self):
        self.album = Album.objects.create(

        )


def urlPreparation(url, urlName, objectId) -> string:
    # url preparation
    if url is None and urlName is None:
        raise "url and urlName is None"

    finalUrl = ""
    if urlName is not None:
        finalUrl = reverse(urlName, kwargs={'pk': objectId})
    if url is not None:
        finalUrl = url + f"{objectId}/"

    return finalUrl


class TestCreateUpdateDeleteAlbum(APITestCase):
    def authenticate(self):
        self.client.post(
            reverse("auth_register"),
            {
                "username": "javid",
                "password": "password##!123",
                "confirmPassword": "password##!123",
                "email": "javid@gmail.com",
                "first_name": "mohammad",
                "last_name": "javid"
            },
        )

        response = self.client.post(reverse('token_obtain_pair'), {
            "username": "javid",
            "password": "password##!123",
        })

        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def createAlbum(self, album, statusCode, itemCheck=None):
        if itemCheck is None:
            response = self.client.post(reverse('album-list'), album)
            self.assertEqual(response.status_code, statusCode)
        else:
            response = self.client.post(reverse('album-list'), album)
            self.assertEqual(response.status_code, statusCode)
            self.assertEqual(response.data[itemCheck], album[itemCheck])

    def countObject(self, url, count, statusCode=None):
        if statusCode is None:
            response = self.client.get(url)
            self.assertEqual(count, response.data['count'])
        else:
            response = self.client.get(url)
            self.assertEqual(statusCode, response.status_code)
            self.assertEqual(count, response.data['count'])

    def updateObject(self, data, objectId, statusCode, url=None, urlName=None):
        finalUrl = urlPreparation(url, urlName, objectId)

        # update data of object
        response = self.client.put(finalUrl, data)
        self.assertEqual(response.status_code, statusCode)

    def deleteObject(self, objectId, statusCode, url=None, urlName=None):
        finalUrl = urlPreparation(url, urlName, objectId)

        # delete object
        response = self.client.delete(finalUrl)
        self.assertEqual(response.status_code, statusCode)

    def showObjects(self, url):
        response = self.client.get(url)
        print("\n\n", response.data, "\n")

    def setUp(self):
        self.valid_album = {
            "title": "nature",
            "artist_name": "maryam",
            "price": 155
        }
        self.valid_album2 = {
            "title": "nature2",
            "artist_name": "ahmadi",
            "price": 199
        }

        self.invalid_album = {
            "title": "nature",
            "artist_name": "maryam",
        }

        self.update_album = self.valid_album
        self.update_album['title'] = "maryam's photo"

        self.update_album2 = self.valid_album2
        self.update_album2['artist_name'] = "wellcome photos"
        self.invalidId = 1999

    def test_create_delete_update_album(self):
        """authenticate user"""
        self.authenticate()

        """Create album"""
        self.createAlbum(album=self.valid_album, statusCode=status.HTTP_201_CREATED, itemCheck='artist_name')
        self.createAlbum(album=self.valid_album2, statusCode=status.HTTP_201_CREATED, itemCheck='title')
        # create invalid album
        self.createAlbum(album=self.invalid_album, statusCode=status.HTTP_400_BAD_REQUEST)

        """List and count"""
        self.countObject(url="/api/v1/albums/", count=2, statusCode=status.HTTP_200_OK)
        self.countObject(url="/api/v1/users/", count=1, statusCode=status.HTTP_200_OK)

        """Update album"""
        albumsResponse = self.client.get("/api/v1/albums/")
        self.updateObject(data=self.update_album,
                          objectId=albumsResponse.data['results'][0]['id'],
                          statusCode=status.HTTP_200_OK,
                          urlName="album-detail")

        self.updateObject(data=self.update_album2,
                          objectId=albumsResponse.data['results'][1]['id'],
                          statusCode=status.HTTP_200_OK,
                          urlName="album-detail")
        # update invalid data album
        self.updateObject(data=self.invalid_album,
                          objectId=albumsResponse.data['results'][1]['id'],
                          statusCode=status.HTTP_400_BAD_REQUEST,
                          urlName="album-detail")
        # update album by invalid id
        self.updateObject(data=self.update_album,
                          objectId=self.invalidId,
                          statusCode=status.HTTP_404_NOT_FOUND,
                          urlName="album-detail")
        # show album after update
        # self.showObjects(url="/api/v1/albums/")

        """Delete album"""
        res = self.client.get("/api/v1/albums/")
        self.deleteObject(objectId=res.data['results'][0]['id'],
                          statusCode=status.HTTP_204_NO_CONTENT,
                          urlName="album-detail")
        # delete album by invalid id
        self.deleteObject(objectId=self.invalidId,
                          statusCode=status.HTTP_404_NOT_FOUND,
                          urlName="album-detail")

        # show all album after delete
        # self.showObjects(url="/api/v1/albums/")


class TestGetSingleUser(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="javid",
            password="javid",
            email="javid@gmail.com",
            first_name="mohammadreza",
            last_name="javid",
        )

        self.use2 = User.objects.create(
            username="ali",
            password="ali",
            email="ali@gmail.com",
            first_name="ali",
            last_name="javid",
        )

    def test_get_valid_single_user(self):
        response = self.client.get(reverse('user-detail', kwargs={'pk': self.user.pk}))
        user = User.objects.get(pk=self.user.pk)
        serializer = UserSerializer(user)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_user(self):
        response = self.client.get(reverse('user-detail', kwargs={'pk': 90}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


"""Test by Factory"""

# class TestAlbum(APITestCase):
#
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.view = AlbumViewSet.as_view({
#             'get': 'list',
#             'post': 'create',
#             'put': 'update',
#             'delete': 'destroy',
#         })
#         self.user = User.objects.create(
#             username="javid",
#             password="javidjavid",
#             email="javid@gmail.com",
#             first_name="mohammadreza",
#             last_name="javid",
#         )
#         self.data = {
#             "creator": "javid",
#             "title": "nature",
#             "artist_name": "maryam",
#             "price": 155,
#             "images": []
#         }
#         self.PK = 0
#
#     def test_Album_view_set(self):
#         """create-album"""
#         self.url = reverse('album-list')
#         request = self.factory.post(self.url, data=self.data)
#         force_authenticate(request, user=self.user)
#         response = self.view(request)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#         """list-album"""
#         self.url = reverse('album-list')
#         request = self.factory.get(self.url)
#         force_authenticate(request, user=self.user)
#         response = self.view(request)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         """get-album"""
#         self.url = reverse('album-detail', args=[1])
#         request = self.factory.get(self.url)
#         force_authenticate(request, user=self.user)
#         response = self.view(request)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['results'][0]['creator'], self.data['creator'])
#         self.PK = response.data['results'][0]['id']
#
#         """update-album"""
#         updateData = self.data
#         updateData['artist_name'] = 'ali'
#
#         self.url = reverse('album-detail', args=[self.PK])
#         request = self.factory.put(self.url, data=updateData)
#         force_authenticate(request, user=self.user)
#         response = self.view(request)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(updateData['artist_name'], 'ali')
#
#         """delete-album"""
#         self.url = reverse('album-detail', args=[self.PK])
#         request = self.factory.delete(self.url)
#         force_authenticate(request, user=self.user)
#         response = self.view(request)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
