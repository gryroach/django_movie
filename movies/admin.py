from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Movie, Member, MovieShots, Genre, Rating, RatingStar, Review

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from modeltranslation.admin import TranslationAdmin


# инициализация CKEditor формы и привязка к полю description
class MovieAdminForm(forms.ModelForm):
    """
    Форма с виджетом ckeditor
    """
    description_ru = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    description_en = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'description', 'url')
    list_display_links = ('name',)


# отображение отзывов в информации о фильмах
class ReviewInLine(admin.TabularInline):
    model = Review
    readonly_fields = ('name', 'email')
    extra = 1


class MovieShotsInLine(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image',)

    # Отображение картикок в админке
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="150" height="120">')

    get_image.short_description = "Изображение"


@admin.register(Movie)
class MovieAdmin(TranslationAdmin):
    list_display = ('title', 'tagline', 'description', 'year', 'country', 'display_director',
                    'display_actor', 'category', 'display_genre', 'premier', 'url', 'draft')
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__name')
    inlines = [MovieShotsInLine, ReviewInLine]
    # Перенос панели сохранения наверх
    save_on_top = True
    # Сохранение как нового объекта без очищения полей
    save_as = True
    fieldsets = ((None, {'fields': ('title', 'tagline', 'description', ('year', 'country', 'premier'), 'genre')}),
                 ('Актеры и режисеры', {'fields': (('director', 'actor'),)}),
                 (None, {'fields': (('budget', 'fees_USA', 'feel_world'), ('poster', 'get_image'))}),
                 ('Прочая информация', {'classes': ('collapse',), 'fields': ('category', 'url', 'draft')}))
    # изменение поля в списке
    list_editable = ('draft',)

    # actions =

    # Подключение формы редактора ckeditor
    form = MovieAdminForm

    # Отображение постера
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="150">')

    get_image.short_description = "Постер"

    actions = ['publish', 'unpublish',]

    # Определение методов дополнительных actions
    def publish(self, request, queryset):
        """ Опубликовать """
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = 'Одна запись была обновлена'
        else:
            message_bit = f'{row_update} записи были обновлены'
        self.message_user(request, message_bit)

    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change',)

    def unpublish(self, request, queryset):
        """ Снять с публикации """
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = 'Одна запись была обновлена'
        else:
            message_bit = f'{row_update} записи были обновлены'
        self.message_user(request, message_bit)

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = ('change',)


@admin.register(Member)
class MemberAdmin(TranslationAdmin):
    list_display = ('name', 'age', 'description', 'get_image')
    readonly_fields = ('get_image',)

    # Отображение картикок в админке
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="120">')

    get_image.short_description = "Изображение"


@admin.register(MovieShots)
class MovieShotsAdmin(TranslationAdmin):
    list_display = ('title', 'description', 'get_image', 'movie')
    readonly_fields = ('get_image',)

    # Отображение картикок в админке
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="150" height="120">')

    get_image.short_description = "Изображение"


@admin.register(Genre)
class GenreAdmin(TranslationAdmin):
    list_display = ('name', 'description', 'url')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('ip', 'movie', 'star')


admin.site.register(RatingStar)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'text', 'parent', 'movie')
    readonly_fields = ('email', 'name')


admin.site.site_title = "Администрирование фильмов"
admin.site.site_header = "Администрирование фильмов"
