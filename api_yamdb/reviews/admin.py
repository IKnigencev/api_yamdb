from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from reviews.models import User, Title, Genre, Category


admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)

admin.site.register(User, UserAdmin)
