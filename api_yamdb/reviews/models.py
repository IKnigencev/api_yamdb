from django.db import models


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=200
    )
    year = models.IntegerField(verbose_name='Год выпуска')
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        'Genre',
        related_name='genre',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        'Category',
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
