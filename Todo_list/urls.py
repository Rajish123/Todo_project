from django.urls import path
from .import views

urlpatterns = [
    path('signup',views.SignUp,name = 'signup'),
    path('login',views.Login,name = 'login'),
    path('logout',views.Logout,name='logout'),
    path('home',views.Index,name = 'home'),
    path('createtodo',views.CreateTodo,name='create-todo'),
    path('todo_detail/<slug:slug>/',views.TodoDetail,name = 'todo-detail'),
    path('update_todo/<slug:slug>/',views.UpdateTodo,name = 'todo-update')
]
