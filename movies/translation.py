from modeltranslation.translator import register, TranslationOptions
from .models import Category, Movie, Member, MovieShots, Genre


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Movie)
class MovieTranslationOptions(TranslationOptions):
    fields = ('title', 'tagline', 'description', 'country')


@register(Member)
class MemberTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(MovieShots)
class MovieShotsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
