from django.shortcuts import render
from django.views.generic import View, ListView, DetailView

from .models import Movie


class MoviesView(ListView):
    """
    Список фильмов
    """
    model = Movie
    queryset = Movie.objects.filter(draft=False)


class MovieDetailView(DetailView):
    """
    Детальное описание фильма
    """
    model = Movie
    slug_field = 'url'
