from django.contrib import admin
from .models import Category, Movie, Member, MovieShots, Genre, Rating, RatingStar, Review
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'url')
    list_display_links = ('name',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'tagline', 'description', 'poster', 'year', 'country', 'display_director',
                    'display_actor', 'category', 'display_genre', 'premier', 'budget', 'fees_USA',
                    'feel_world', 'url', 'draft')


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
