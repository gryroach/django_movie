from django.db import models
from datetime import date

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    """
    Категории
    """
    name = models.CharField("Категория", max_length=45, null=False)
    description = models.TextField("Описание", null=True)
    url = models.SlugField(max_length=150, unique=True)

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Member(models.Model):
    """
    Актеры и режиссеры
    """
    name = models.CharField("Имя", max_length=100, null=True)
    age = models.PositiveSmallIntegerField("Возраст", null=True, default=0)
    description = models.TextField("Описание", null=True)
    image = models.ImageField("Изображение", upload_to="members/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Актеры и режиссеры"
        verbose_name_plural = "Актеры и режиссеры"


class Genre(models.Model):
    """
    Жанры
    """
    name = models.CharField("Жанр", max_length=45)
    description = models.TextField("Описание", null=True)
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Movie(models.Model):
    """
    Фильм
    """
    title = models.CharField("Название", max_length=45, null=False)
    tagline = models.CharField("Слоган", max_length=45, default='')
    description = models.TextField("Описание", null=True)
    poster = models.ImageField("Постер", upload_to="posters/", height_field=None, width_field=None, max_length=100)
    year = models.SmallIntegerField("Год", null=True, default=2010)
    country = models.CharField("Страна", max_length=45, null=True)
    director = models.ManyToManyField(Member, verbose_name="режиссер",
                                      related_name="film_director")
    actor = models.ManyToManyField(Member, verbose_name="актер",
                                   related_name="film_actor")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Категория")
    genre = models.ManyToManyField(Genre, verbose_name="Жанры")
    premier = models.DateField("Премьера в мире", max_length=45, null=True, default=date.today)
    budget = models.PositiveIntegerField("Бюджет", null=True, default=0,
                                         help_text="указывать сумму в долларах")
    fees_USA = models.IntegerField("Сборы в США", null=True, default=0,
                                   help_text="указывать сумму в долларах")
    feel_world = models.IntegerField("Сборы в мире", null=True, default=0,
                                     help_text="указывать сумму в долларах")
    url = models.SlugField(max_length=150, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "фильм"
        verbose_name_plural = "фильмы"

    def get_review(self):
        return self.review_set.filter(parent__isnull=True)

    def display_actor(self):
        """
        Список актеров
        """
        return ', '.join([actor.name for actor in self.actor.all()])
    display_actor.short_description = 'actor'

    def display_director(self):
        """
        Список режисеров
        """
        return ', '.join([director.name for director in self.director.all()])
    display_director.short_description = 'director'

    def display_genre(self):
        """
        Список жанров
        """
        return ', '.join([genre.name for genre in self.genre.all()])
    display_genre.short_description = 'genre'

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug': self.url})


class MovieShots(models.Model):
    """
    Кадры из фильма
    """
    title = models.CharField("Заголовок", max_length=45, null=True)
    description = models.TextField("Описание", null=True)
    image = models.ImageField("Изображение", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Фильм")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильма"


class Review(models.Model):
    """
    Отзывы к фильму
    """
    email = models.EmailField("Почта", max_length=45)
    name = models.CharField("Имя", max_length=45, null=True)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey('self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Фильм")

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class RatingStar(models.Model):
    """
    Звезда рейтинга
    """
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"


class Rating(models.Model):
    """
    Рейтинг
    """
    ip = models.CharField("IP адрес", max_length=15, blank=True, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Фильм")
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"
