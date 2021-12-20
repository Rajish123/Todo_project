from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('signup',views.SignUp,name = 'signup'),
    path('login',auth_views.LoginView.as_view(template_name = 'Todo_list/login.html'),name = 'login'),
    path('logout',auth_views.LogoutView.as_view(),name='logout'),
    path('profile',views.Profile,name = 'profile'),
    path('profile_settings', views.UpdateProfile, name = 'update_profile'),
    path('home',views.Index,name = 'home'),
    path('createtodo',views.CreateTodo,name='create-todo'),
    path('todo_detail/<slug:slug>/',views.TodoDetail,name = 'todo-detail'),
    path('update_todo/<slug:slug>/',views.UpdateTodo,name = 'todo-update'),
    path('list_todo',views.ListTodo,name = 'todo-list'),
    path('delete_todo/<slug:slug>/',views.DeleteTodo,name = 'delete-todo'),
    path('accomplished',views.AccomplishedTodo,name = 'todo-accomplished'),
    path('iinprogress', views.TodoInprogress,name = 'todo-inprogress'),
    path('log',views.TodoLog,name = 'log'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
