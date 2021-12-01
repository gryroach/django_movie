from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView

from .models import Movie, Category, Member

from .forms import ReviewForm


class MoviesView(ListView):
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


class MovieDetailView(DetailView):
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


class MemberDetail(DetailView):
    model = Member
    template_name = 'movies/member.html'
    slug_field = 'name'
