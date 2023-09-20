from rest_framework import serializers
from .models import Album, AlbumImage
from django.contrib.auth.models import User


class AlbumImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumImage
        fields = ['id', 'album', 'image']


class AlbumSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    images = AlbumImageSerializer(many=True, read_only=True, required=False)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Album
        fields = ['id', 'creator', 'title', 'artist_name',
                  'price', 'images', 'uploaded_images']

    def create(self, validated_data):
        if 'uploaded_images' in validated_data:
            uploaded_images = validated_data.pop("uploaded_images")
            album = Album.objects.create(**validated_data)
            for image in uploaded_images:
                newAlbumImage = AlbumImage.objects.create(album=album, image=image)
            return album
        else:
            album = Album.objects.create(**validated_data)
            return album


class UserSerializer(serializers.ModelSerializer):
    albums = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Album.objects.all()
    )

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'albums']
        read_only_fields = ['albums', 'username']
