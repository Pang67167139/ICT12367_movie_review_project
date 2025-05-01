from django.urls import path
from . import views

urlpatterns = [
    path('', views.MovieListView.as_view(), name='home'),
    path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
    path('movie/new/', views.MovieCreateView.as_view(), name='movie-create'),
    path('movie/<int:pk>/update/', views.MovieUpdateView.as_view(), name='movie-update'),
    path('movie/<int:pk>/delete/', views.MovieDeleteView.as_view(), name='movie-delete'),
    path('movie/<int:pk>/review/', views.add_review, name='add-review'),
    path('review/<int:pk>/edit/', views.edit_review, name='edit-review'),
    path('review/<int:pk>/delete/', views.delete_review, name='delete-review'),
]