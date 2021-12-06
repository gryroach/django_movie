from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView

from .models import Movie, Category, Member, Genre, Rating, RatingStar

from .forms import ReviewForm, RatingForm


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
    paginate_by = 1

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
    queryset = Movie.objects.filter(draft=False)
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        context["form"] = ReviewForm()
        return context


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
    paginate_by = 1

    def get_queryset(self):
        # вернуть список, отфильтрованный запросом в форму фронта с переменной year
        # метод Q необходим для срабатывания "ИЛИ"
        queryset = Movie.objects.filter(Q(year__in=self.request.GET.getlist("year")) |
                                        Q(genre__in=self.request.GET.getlist("genre"))
                                        ).distinct()    # distinct - для удаления повторяющихся элементов
        return queryset

    # настройка для пагинации при фильтации
    def get_context_data(self, *args, **kwargs):
        context = super(FilterMovieView, self).get_context_data(*args, **kwargs)
        context['year'] = ''.join([f'year={x}&' for x in self.request.GET.getlist("year")])
        context['genre'] = ''.join([f'genre={x}&' for x in self.request.GET.getlist("genre")])
        return context


# фильтр без обновления страницы через json
class JsonFilterMoviesView(ListView):
    """
    Фильтр фильмов в json
    """
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genre__in=self.request.GET.getlist("genre"))
        ).distinct().values("title", "tagline", "url", "poster")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movies": queryset}, safe=False)


class AddStarRating(View):
    """
    Добавление рейтинга к фильму
    """
    def get_client_ip(self, request):
        """ Получение IP-адреса пользователя """
        x_forwarded_for = request.META.get("HTTP_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            # добавление записи или обновление, если существует
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get('movie')),
                defaults={'star_id': int(request.POST.get('star'))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class Search(ListView, GenreYear):
    """
    Поиск фильмов
    """
    paginate_by = 1

    def get_queryset(self):
        q = self.request.GET.get('q').capitalize()  #   capitalize для работы посика с маленькой буквы в SQLite
        return Movie.objects.filter(title__icontains=q)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context
