from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # แก้ไขบรรทัดนี้เพื่อเพิ่ม http_method_names
    path('logout/', auth_views.LogoutView.as_view(
        template_name='users/logout.html',
        http_method_names=['get', 'post']  # อนุญาตทั้ง GET และ POST
    ), name='logout'),
    path('profile/', views.profile, name='profile'),
]