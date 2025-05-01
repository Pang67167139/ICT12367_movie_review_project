from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Movie, Review
from .forms import ReviewForm, MovieForm
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied

class MovieListView(ListView):
    model = Movie
    template_name = 'reviews/home.html'
    context_object_name = 'movies'
    ordering = ['-created_at']
    paginate_by = 8
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # รับพารามิเตอร์การค้นหาจาก GET request
        title = self.request.GET.get('title')
        director = self.request.GET.get('director')
        genre = self.request.GET.get('genre')
        year = self.request.GET.get('year')
        
        # สร้าง query ตามเงื่อนไขการค้นหา
        if title:
            queryset = queryset.filter(title__icontains=title)
        if director:
            queryset = queryset.filter(director__icontains=director)
        if genre:
            queryset = queryset.filter(genre__icontains=genre)
        if year:
            queryset = queryset.filter(release_year=year)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # สร้างข้อความแสดงการค้นหา
        search_params = []
        if self.request.GET.get('title'):
            search_params.append(f"ชื่อ: {self.request.GET.get('title')}")
        if self.request.GET.get('director'):
            search_params.append(f"ผู้กำกับ: {self.request.GET.get('director')}")
        if self.request.GET.get('genre'):
            search_params.append(f"ประเภท: {self.request.GET.get('genre')}")
        if self.request.GET.get('year'):
            search_params.append(f"ปี: {self.request.GET.get('year')}")
            
        if search_params:
            context['search_query'] = ', '.join(search_params)
            
        return context

class MovieDetailView(DetailView):
    model = Movie
    template_name = 'reviews/movie_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all().order_by('-date_posted')
        context['review_form'] = ReviewForm()
        
        # ตรวจสอบว่าผู้ใช้เป็น admin หรือไม่
        context['is_admin'] = self.request.user.groups.filter(name='Admins').exists() or self.request.user.is_superuser
        
        return context

class MovieCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'reviews/movie_form.html'
    permission_required = 'reviews.add_movie'
    
    def form_valid(self, form):
        messages.success(self.request, 'ภาพยนตร์ถูกเพิ่มเรียบร้อยแล้ว!')
        return super().form_valid(form)
    
    def handle_no_permission(self):
        messages.error(self.request, 'คุณไม่มีสิทธิ์เพิ่มภาพยนตร์ กรุณาติดต่อผู้ดูแลระบบ')
        return redirect('home')

class MovieUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = 'reviews/movie_form.html'
    permission_required = 'reviews.change_movie'
    
    def form_valid(self, form):
        messages.success(self.request, 'ข้อมูลภาพยนตร์ถูกอัปเดตเรียบร้อยแล้ว!')
        return super().form_valid(form)
    
    def handle_no_permission(self):
        messages.error(self.request, 'คุณไม่มีสิทธิ์แก้ไขภาพยนตร์ กรุณาติดต่อผู้ดูแลระบบ')
        return redirect('movie-detail', pk=self.kwargs.get('pk'))

class MovieDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Movie
    template_name = 'reviews/movie_confirm_delete.html'
    success_url = reverse_lazy('home')
    permission_required = 'reviews.delete_movie'
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'ภาพยนตร์ถูกลบเรียบร้อยแล้ว!')
        return super().delete(request, *args, **kwargs)
    
    def handle_no_permission(self):
        messages.error(self.request, 'คุณไม่มีสิทธิ์ลบภาพยนตร์ กรุณาติดต่อผู้ดูแลระบบ')
        return redirect('movie-detail', pk=self.kwargs.get('pk'))

@login_required
def add_review(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.author = request.user
            review.save()
            messages.success(request, 'รีวิวของคุณถูกเพิ่มเรียบร้อยแล้ว!')
            return redirect('movie-detail', pk=movie.pk)
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/review_form.html', {'form': form, 'movie': movie})

@login_required
def edit_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    
    # ตรวจสอบว่าผู้ใช้เป็นเจ้าของรีวิวหรือเป็น admin
    if request.user != review.author and not (request.user.groups.filter(name='Admins').exists() or request.user.is_superuser):
        messages.error(request, 'คุณไม่มีสิทธิ์แก้ไขรีวิวนี้!')
        return redirect('movie-detail', pk=review.movie.pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'รีวิวของคุณถูกอัปเดตเรียบร้อยแล้ว!')
            return redirect('movie-detail', pk=review.movie.pk)
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'reviews/review_form.html', {'form': form, 'movie': review.movie, 'edit': True})

@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    
    # ตรวจสอบว่าผู้ใช้เป็นเจ้าของรีวิวหรือเป็น admin
    if request.user != review.author and not (request.user.groups.filter(name='Admins').exists() or request.user.is_superuser):
        messages.error(request, 'คุณไม่มีสิทธิ์ลบรีวิวนี้!')
        return redirect('movie-detail', pk=review.movie.pk)
    
    movie_pk = review.movie.pk
    review.delete()
    messages.success(request, 'รีวิวของคุณถูกลบเรียบร้อยแล้ว!')
    return redirect('movie-detail', pk=movie_pk)