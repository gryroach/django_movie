from django import template
from movies.models import Category, Movie


# регистрация темплейт-тэгов
register = template.Library()


@register.simple_tag()
def get_category():
    """ Вывод всех категорий """
    return Category.objects.all()


@register.inclusion_tag('movies/tags/last_movie.html')
def get_last_movies(count=5):
    """ Вывод последних count фильмов """
    movies = Movie.objects.order_by('id')[:count]
    return {'last_movies': movies}
