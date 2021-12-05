from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path("", views.MoviesView.as_view(), name='movie_view'),
]

urlpatterns += [
    path("filter/", views.FilterMovieView.as_view(), name='filter')
]
# фильтр без обновления страницы через json
urlpatterns += [
    path("json-filter/", views.JsonFilterMoviesView.as_view(), name='json_filter')
]

urlpatterns += [
    # url("^movie/(?P<pk>\d+)$", views.MovieDetailView.as_view(), name='movie_detail')
    path("movie/<slug:slug>/", views.MovieDetailView.as_view(), name='movie_detail')
]

urlpatterns += [
    path("review/<int:pk>/", views.AddReview.as_view(), name='add_review')
]

urlpatterns += [
    path("members/<str:slug>/", views.MemberDetail.as_view(), name='member_detail')
]

urlpatterns += [
    path("add_rating/", views.AddStarRating.as_view(), name='add_rating')
]


