from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .filters import *
from django.contrib.auth import authenticate,login

# Create your views here.

def SignUp(request):
    context = {}
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password1')
            user = form.save()
            login(request, user)
            messages.success(request,f"{username} account successfully created")
            # new_user = authenticate(username = username, password = password)
            # if new_user is not None:
                # login(request,new_user)
            return redirect('home')
        messages.error(request,"Not a valid form")
    else:
        form = UserRegistrationForm()
    context['form'] = form
    return render(request,'Todo_list/signup.html',context)

def Index(request):
    return render(request,'Todo_list/index.html')

@login_required
def Profile(request):
    return render(request,'Todo_list/profile.html')   

@login_required
def UpdateProfile(request):
    context = {}
    if request.method == "POST":
        # interacts with the user model to let users update their username and email
        userform = UserUpdateForm(request.POST, instance=request.user)
        # interacts with the profile model to let users update their profile
        profileform = ProfileUpdateForm(request.POST,request.FILES, instance=request.user.profile)
        if userform and profileform.is_valid():
            userform.save()
            profileform.save()
            messages.success(request,"Updated Successful")
            return redirect('profile')
        else:
            messages.error(request,"Not valid!")
    else:
        userform = UserUpdateForm(instance=request.user)
        profileform = ProfileUpdateForm(instance = request.user.profile)
    context = {'userform':userform,'profileform':profileform}
    return render(request,'Todo_list/settings.html',context)


@login_required
def CreateTodo(request):
    context = {}
    
    if request.method == "POST":
        todoform = TodoForm(request.POST)
        todoform.instance.profile = request.user.profile

        if todoform.is_valid():
            todoform.save()
            messages.success(request,"Successfully Created.")
            return redirect('home')
        else:
            messages.error(request,"Form you filled is not a valid one!!")
            return redirect('create-todo')
    else:
        todoform = TodoForm(instance=request.user)
    context = {'form': todoform}
    return render(request,'Todo_list/createtodo.html',context)

@login_required
def TodoDetail(request,slug):
    context = {}
    todo = get_object_or_404(Todo,slug = slug)
    context['todo'] = todo
    return render(request,'Todo_list/todo_detail.html',context)

@login_required
def UpdateTodo(request,slug):
    context = {}
    todo = Todo.objects.get(slug__iexact = slug)
    if request.method == "POST":
        update_form = TodoForm(request.POST, instance=todo)
        if update_form.is_valid():
            update_form.save()
            messages.success(request,"Updated Successfully")
            return redirect('todo-detail', slug = todo.slug)
    else:
        update_form = TodoForm(instance = todo)
    context['form'] = update_form
    return render(request,'Todo_list/update_todo.html',context)

@login_required
def ListTodo(request):
    context = {}
    profile = request.user.profile
    todo_list = profile.todo_set.all()
    # here data get rendered in todo_list which is thrown in myFilter and if we have any parameters it filters
    # it down and then we remake the filterdata and assign to variable in todolist in line 96
    myFilter = SearchFilter(request.GET, queryset = todo_list)
    todo_list = myFilter.qs
    context = {'todo_list': todo_list, 'myFilter': myFilter}
    return render(request,"Todo_list/listtodo.html",context)

@login_required
def DeleteTodo(request,slug):
    todo_to_delete = Todo.objects.get(slug__iexact = slug)
    todo_to_delete.delete()
    messages.success(request,f"{todo_to_delete.title} successfully deleted")
    return redirect('todo-list')

@login_required
def AccomplishedTodo(request):
    context = {}
    profile = request.user.profile
    todo_completed = profile.todo_set.filter(completed = "Accomplished")
    myFilter = SearchFilter(request.GET, queryset = todo_completed)
    todo_completed = myFilter.qs
    context = {'todo_completed':todo_completed, 'myFilter': myFilter}
    return  render(request,'Todo_list/accomplished_todo.html',context)

@login_required
def TodoInprogress(request):
    context = {}
    profile = request.user.profile
    todo_inprogress = profile.todo_set.filter(completed = "Unaccomplished")
    myFilter = SearchFilter(request.GET, queryset = todo_inprogress)
    todo_inprogress = myFilter.qs
    context = {'todo_inprogress':todo_inprogress, 'myFilter': myFilter}
    return render(request,'Todo_list/todo_inprogress.html',context)

@login_required
def TodoLog(request):
    context = {}
    profile = request.user.profile
    all_todo = profile.todo_set.all()
    todo_completed = profile.todo_set.filter(completed = "Accomplished")
    inprogress_todo = profile.todo_set.filter(completed = "Unaccomplished")
    all_todo_count = all_todo.count()
    todo_completed_count = todo_completed.count()
    inprogress_todo_count = inprogress_todo.count()
    context = {'todo':all_todo_count, 'todo_completed':todo_completed_count, 'todo_inprogress':inprogress_todo_count}
    return render(request,'Todo_list/todo_log.html',context)








