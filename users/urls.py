from django.urls import path
from . import views  # Імпортуємо весь файл views, щоб звертатися через views.назва

urlpatterns = [
    # Авторизація
    path('', views.login_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Дашборди (головні сторінки)
    path('dashboard/', views.dashboard, name='dashboard'),
    path('teacher/', views.dashboard, name='teacher_dashboard'), 
    
    # Списки (твоя робота з моделями)
    path('branches/', views.branch_list_view, name='branch_list'),
    path('groups/', views.group_list_view, name='group_list'),
    path('students/', views.student_list_view, name='student_list'),
    path('subjects/', views.subject_list_view, name='subject_list'),
]