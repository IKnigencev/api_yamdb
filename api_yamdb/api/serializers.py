from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from django.core.validators import MaxValueValidator, MinValueValidator

from reviews.models import User, Category, Genre, Title, Comment, Review


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


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    title = SlugRelatedField(slug_field='title', read_only=True)
    score = serializers.IntegerField(
        validators=(MinValueValidator(1),
                    MaxValueValidator(10))
    )

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        request = self.context['request']
        title = get_object_or_404(
            Title, pk=self.context.get('view').kwargs.get('title_id')
        ),
        author = request.user
        if (request.method not in ('GET', "PATCH")
           and Review.objects.filter(
                title=title, author=author).exists()):
            raise ValidationError('you already have a review')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)
