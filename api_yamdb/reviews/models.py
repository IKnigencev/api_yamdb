
from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models


class User(AbstractUser):
    admin = 'admin'
    moderator = 'moderator'
    user = 'user'
    ROLES = [
        (admin, 'admin'),
        (moderator, 'moder'),
        (user, 'user')
    ]
    username = models.CharField(
        max_length=150,
        verbose_name='username',
        unique=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+\z',
            message='The user name contains an invalid character'
        )]
    )
    email = models.EmailField(
        verbose_name='email',
        unique=True,
        max_length=254
    )
    first_name = models.CharField(
        verbose_name='first_name',
        max_length=150
    )
    last_name = models.CharField(
        verbose_name='last_name',
        max_length=150
    )
    role = models.CharField(
        verbose_name='role',
        choices=ROLES,
        default=user
    )
    bio = models.TextField(
        verbose_name='User description',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class CommonFieldS(models.Model):
    author = models.ForeignKey(
        'User', on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField('Текст')

    class Meta:
        abstract = True


class Review(CommonFieldS):
    title = models.ForeignKey(
        'Title', on_delete=models.CASCADE,
        verbose_name='Title'
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
                fields=['author', 'title'],
                name='unique_author_review'
            )
        ]
        default_related_name = 'review'
        verbose_name = 'review'

    def __str__(self):
        return self.text[0:30]


class Comment(CommonFieldS):
    review = models.ForeignKey(
        'Review', on_delete=models.CASCADE,
        verbose_name='Comment'
    )

    class Meta:
        default_related_name = 'comment'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.text[0:30]
