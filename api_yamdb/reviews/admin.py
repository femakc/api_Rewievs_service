from django.contrib import admin

from .models import Category, Genre, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pub_date', 'author')


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
