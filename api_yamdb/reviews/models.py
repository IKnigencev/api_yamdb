from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

from django.db import models


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


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
        verbose_name='Название произведения',
        null=True,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        verbose_name='Жанр',
        null=True,
    )

    def __str__(self):
        return f'{self.genre} {self.title}'


class CommonFields(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    class Meta:
        abstract = True


class Review(CommonFields):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Title',
    )
    score = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1),
                    MaxValueValidator(10)),
        error_messages={'validators': 'The scores can be from 1 to 10'},
        default=1
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_author_review'
            )
        ]
        default_related_name = 'reviews'
        verbose_name = 'review'

    def __str__(self):
        return self.text[0:30]


class Comment(CommonFields):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        verbose_name='Comment',
        related_name='comments'
    )

    class Meta:
        default_related_name = 'comments'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.text[0:30]
