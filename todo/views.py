from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, TODOForm
from .models import TODO
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Count, Q

@staff_member_required
def all_todos_admin(request):
    todos = TODO.objects.all().order_by('-created_at')
    return render(request, 'todo/all_todos_admin.html', {'todos': todos})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'todo/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('todo_list')
        else:
            return render(request, 'todo/login.html', {'error': 'Invalid credentials'})
    return render(request, 'todo/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def todo_list(request):
    todos = TODO.objects.filter(user=request.user)
    return render(request, 'todo/todo_list.html', {'todos': todos})

@login_required
def add_todo(request):
    if request.method == 'POST':
        form = TODOForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('todo_list')
    else:
        form = TODOForm()
    return render(request, 'todo/add_todo.html', {'form': form})

@login_required
def delete_todo(request, pk):
    todo = TODO.objects.get(id=pk, user=request.user)
    todo.delete()
    return redirect('todo_list')


@staff_member_required
def admin_dashboard(request):
    total_todos = TODO.objects.count()
    completed_todos = TODO.objects.filter(completed=True).count()
    pending_todos = total_todos - completed_todos
    user_count = User.objects.count()

    top_users = User.objects.annotate(todo_count=Count('todo')).order_by('-todo_count')[:5]

    context = {
        'total_todos': total_todos,
        'completed_todos': completed_todos,
        'pending_todos': pending_todos,
        'user_count': user_count,
        'top_users': top_users,
    }
    return render(request, 'todo/admin_dashboard.html', context)
