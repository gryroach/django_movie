from django.contrib import admin
from .models import Category, Movie, Member, MovieShots, Genre, Rating, RatingStar, Review
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'url')
    list_display_links = ('name',)


# отображение отзывов в информации о фильмах
class ReviewInLine(admin.StackedInline):
    model = Review
    readonly_fields = ('name', 'email')
    extra = 1


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'tagline', 'description', 'year', 'country', 'display_director',
                    'display_actor', 'category', 'display_genre', 'premier', 'url', 'draft')
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__name')
    inlines = [ReviewInLine]
    # Перенос панели сохранения наверх
    save_on_top = True
    # Сохранение как нового объекта без очищения полей
    save_as = True
    fieldsets = ((None, {'fields': ('title', 'tagline', 'description', ('year', 'country', 'premier'), 'genre')}),
                 ('Актеры и режисеры', {'fields': (('director', 'actor'),)}),
                 (None, {'fields': (('budget', 'fees_USA', 'feel_world'), 'poster')}),
                 ('Прочая информация', {'classes': ('collapse',), 'fields': ('category', 'url', 'draft')}))
    # изменение поля в списке
    list_editable = ('draft',)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'description', 'image')


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image', 'movie')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'url')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('ip', 'movie', 'star')


admin.site.register(RatingStar)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'text', 'parent', 'movie')
    readonly_fields = ('email', 'name')
