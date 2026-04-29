from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout 
from courses.models import Student, Branch, StudentGroup, Subject 
from .models import CustomUser 
from django.db.models import Q

def login_view(request):
    if request.method == 'POST':
        login_data = request.POST.get('phone') # Це дані з поля вводу
        password = request.POST.get('password')

        try:
            # Шукаємо користувача: або по email, або по телефону
            user_obj = CustomUser.objects.get(Q(email=login_data) | Q(phone=login_data))
            
            # Оскільки в моделі USERNAME_FIELD = 'email', передаємо його email
            user = authenticate(request, email=user_obj.email, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'registration/login.html', {'error': 'Неправильний пароль'})
        
        except CustomUser.DoesNotExist:
            return render(request, 'registration/login.html', {'error': 'Користувача не знайдено'})

    return render(request, 'registration/login.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Вказуємо шлях до папки dashboard
    if request.user.role == 'teacher':
        return render(request, 'dashboard/teacher.html')
    else:
        return render(request, 'dashboard/admin.html')
    
def student_list_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    students = Student.objects.all() 
    # Вказуємо шлях до папки core
    return render(request, 'core/student_list.html', {'students': students})

def branch_list_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    branches = Branch.objects.all() 
    # Вказуємо шлях до папки core
    return render(request, 'core/branch_list.html', {'branches': branches})

def group_list_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    groups = StudentGroup.objects.all()
    # Вказуємо шлях до папки core
    return render(request, 'core/group_list.html', {'groups': groups})

def subject_list_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    subjects = Subject.objects.all()
    # Вказуємо шлях до папки core
    return render(request, 'core/subject_list.html', {'subjects': subjects})

def logout_view(request):
    logout(request)
    return redirect('login')