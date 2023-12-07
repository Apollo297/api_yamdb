from django.contrib import admin

from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)


class GenreTitleInline(admin.TabularInline):
    model = GenreTitle
    extra = 0


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'category',
        'description',
        'get_genre',
    )
    search_fields = ('name',)
    list_editable = ('category',)
    list_filter = ('name',)
    inlines = [GenreTitleInline]
    exclude = ('genre',)

    @admin.display(description='genres')
    def get_genre(self, obj):
        return [genre.name for genre in obj.genre.all()]


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'genre',
        'title',
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('genre',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'author',
        'score',
    )
    search_fields = ('pub_date',)
    list_filter = ('pub_date',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review',
        'text',
        'author',
        'pub_date',
    )
    search_fields = ('review',)
    list_filter = ('review',)


admin.site.empty_value_display = '-пусто-'
