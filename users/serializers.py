from rest_framework.serializers import ModelSerializer, StringRelatedField, SerializerMethodField
from rest_framework.exceptions import ParseError

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser
from posts.serializers import TinyPostSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(self, user):
        token = super().get_token(user)
        token["email"] = user.email

        return token


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "password",
            "is_active",
            "is_superuser",
        )

    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password

        if password is None:
            raise ParseError

        user.set_password(password)
        user.save()

        return user


class UserDetailSerializer(ModelSerializer):

    followings = StringRelatedField(many=True, read_only=True,)
    followers = StringRelatedField(many=True, read_only=True,)
    posts = TinyPostSerializer(
        many=True,
        read_only=True,
    )
    like_posts = TinyPostSerializer(
        many=True,
        read_only=True,
    )

    def get_posts(self, user):
        return user.posts

    class Meta:
        model = CustomUser
        fields = "id", "email", "followings", "followers", "posts", "like_posts",

    def update(self, user, validated_data):
        user = super().update(user, validated_data)
        password = user.password

        if password is None:
            raise ParseError

        user.set_password(password)
        user.save()

        return user
