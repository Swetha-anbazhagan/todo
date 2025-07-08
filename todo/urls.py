from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup_view, name='signup'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('todos/', views.todo_list, name='todo_list'),
    path('add/', views.add_todo, name='add_todo'),
    path('delete/<int:pk>/', views.delete_todo, name='delete_todo'),
    path('all-todos/', views.all_todos_admin, name='all_todos_admin'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  # ✅ MUST be here
]


