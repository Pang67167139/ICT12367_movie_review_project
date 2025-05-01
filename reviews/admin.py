from django.contrib import admin
from .models import Movie, Review

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'release_year', 'genre', 'created_at')
    list_filter = ('genre', 'release_year')
    search_fields = ('title', 'director', 'plot')
    date_hierarchy = 'created_at'
    inlines = [ReviewInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'author', 'rating', 'date_posted')
    list_filter = ('rating', 'date_posted')
    search_fields = ('content', 'movie__title', 'author__username')