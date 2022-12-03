from django.db import models
from django.contrib.auth.models import AbstractUser


ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    """Кастомная модель юзера с ролями"""

    username = models.CharField(
        max_length=150,
        verbose_name='username',
        unique=True,
        null=True,
    )
    mail = models.EmailField(
        max_length=255,
        verbose_name='Введите email'
    )
    role = models.CharField(
        max_length=11,
        choices=ROLE_CHOICES,
        default='user'
    )
    bio = models.CharField(
        max_length=50,
        default='',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.role

    @property
    def is_admin(self):
        """Проверка на роль администратора"""
        if self.role == 'admin':
            return True
        return False

    @property
    def is_user(self):
        """Проверка на роль обычного юзера"""
        if self.role == 'user':
            return True
        return False

    @property
    def is_moderator(self):
        """Проверка на роль модератора"""
        if self.role == 'moderator':
            return True
        return False


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Жанр',
        max_length=250,
        unique=True)
    slug = models.SlugField(
        max_length=30,
        unique=True)

    class Meta:
        verbose_name = 'Жанр'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name='Название')
    slug = models.SlugField(
        max_length=50,
        unique=True)

    class Meta:
        verbose_name = 'Категория'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=200
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genre',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='category',
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'Название произведения'
        ordering = ('-year',)

    def __str__(self):
        return self.name
