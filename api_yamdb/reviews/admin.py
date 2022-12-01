from django.contrib import admin

from reviews.models import Comment, Review, User


class UserAdmin(admin.ModelAdmin):
    list_display = ("pk", "username", "email", "role", "bio")
    search_fields = ("username",)
    list_filter = ("role",)
    list_editable = ("username", "email", "role", "bio")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("title", "text", "score")
    search_fields = ("title",)
    list_filter = ("score",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("review", "text")
    search_fields = ("review",)


admin.site.register(User, UserAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
