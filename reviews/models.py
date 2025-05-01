from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Movie(models.Model):
    title = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    release_year = models.IntegerField()
    genre = models.CharField(max_length=50)
    poster = models.ImageField(upload_to='movie_posters', default='default_poster.jpg')
    plot = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('movie-detail', kwargs={'pk': self.pk})

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - แย่มาก'),
        (2, '2 - แย่'),
        (3, '3 - พอใช้'),
        (4, '4 - ดี'),
        (5, '5 - ดีมาก'),
    ]
    
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'รีวิว {self.movie.title} โดย {self.author.username}'
    
    def get_absolute_url(self):
        return reverse('movie-detail', kwargs={'pk': self.movie.pk})