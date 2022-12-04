from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import *


class UserSerializer(serializers.ModelSerializer):
    """Сериализация модели юзера"""

    username = serializers.CharField(
        required=True,
        validators=(
            UniqueValidator(queryset=User.objects.all()),
        )
    )
    email = serializers.EmailField(
        required=True,
        validators=(
            UniqueValidator(queryset=User.objects.all()),
        )
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'role',
            'first_name',
            'last_name',
            'bio'
        )


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализация авторизации"""

    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать username me')
        elif User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Такой пользователь уже существует')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует')
        return value


class TokenSerializer(serializers.ModelSerializer):
    """Сериализация токена авторизации"""

    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('confirmation_code', 'username')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = "__all__"
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True, slug_field="slug", queryset=Genre.objects.all()
    )

    class Meta:
        fields = "__all__"
        model = Title
