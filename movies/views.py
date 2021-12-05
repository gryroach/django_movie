from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView

from .models import Movie, Category, Member, Genre

from .forms import ReviewForm


class GenreYear:
    """
    Жанры и года
    """
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):

        years = set()
        years_list = Movie.objects.filter(draft=False).values("year")   # вернуть элементы с именем поля "year"
        for year in years_list:
            years.add(year['year'])
        return sorted(years, reverse=True)
        # return Movie.objects.filter(draft=False)


class MoviesView(ListView, GenreYear):
    """
    Список фильмов
    """
    model = Movie
    queryset = Movie.objects.filter(draft=False)

    # # добавление объектов категорий к списку фильмов
    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['categories'] = Category.objects.all()
    #     return context


class MovieDetailView(DetailView, GenreYear):
    """
    Детальное описание фильма
    """
    model = Movie
    slug_field = 'url'


class AddReview(View):
    """
    Отправка отзывов
    """
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class MemberDetail(DetailView, GenreYear):
    model = Member
    template_name = 'movies/member.html'
    slug_field = 'name'


class FilterMovieView(GenreYear, ListView):
    """
    Фильтр фильмов по годам
    """
    def get_queryset(self):
        # вернуть список, отфильтрованный запросом в форму фронта с переменной year
        # метод Q необходим для срабатывания "ИЛИ"
        queryset = Movie.objects.filter(Q(year__in=self.request.GET.getlist("year")) |
                                        Q(genre__in=self.request.GET.getlist("genre"))
                                        )
        return queryset
