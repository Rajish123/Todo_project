from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .filters import *

# Create your views here.

def SignUp(request):
    context = {}
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request,f"{username} account successfully created")
            return redirect('home')
    else:
        form = UserRegistrationForm(request.GET)
    context['form'] = form
    return render(request,'Todo_list/signup.html',context)

def Index(request):
    return render(request,'Todo_list/index.html')

@login_required
def Profile(request):
    context = {}
    if request.method == "POST":
        userform = UserUpdateForm(request.POST, instance=request.user)
        profileform = ProfileUpdateForm(request.POST,request.FILES,instance = request.user.profile)
        if userform and profileform.is_valid():
            userform.save()
            profileform.save()
            messages.success(request,"Profile updated successfully")
            return redirect('home')
        else:
            messages.error(request,"Not a valid form")
            return redirect('home')
    else:
        userform = UserUpdateForm(instance = request.user)
        profileform = ProfileUpdateForm(instance = request.user.profile)
    context['userform'] = userform
    context['profileform'] = profileform
    return render(request,'Todo_list/profile.html',context)            

@login_required
def CreateTodo(request):
    context = {}
    if request.method == "POST":
        todoform = TodoForm(request.POST,instance=request.user.profile)
        if todoform.is_valid():
            todoform.save()
            messages.success(request,"Successfully Created.")
            return redirect('home')
        else:
            messages.error(request,"Form you filled is not a valid one!!")
            return redirect('create-todo')
    else:
        todoform = TodoForm()
    context['form'] = todoform
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
        update_form = TodoForm()
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









