from django.contrib import admin
from siimapp.models import FavouritePost, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title',]


admin.site.register(FavouritePost)