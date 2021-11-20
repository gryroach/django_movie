from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path("", views.MoviesView.as_view(), name='movie_view')
]

urlpatterns += [
    # url("^movie/(?P<pk>\d+)$", views.MovieDetailView.as_view(), name='movie_detail')
    path("movie/<slug:slug>/", views.MovieDetailView.as_view(), name='movie_detail')
]

urlpatterns += [
    path("review/<int:pk>/", views.AddReview.as_view(), name='add_review')
]
