from django.http.response import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.

def SignUp(request):
    signup_form = SignUpForm(request.POST or None)
    if signup_form.is_valid():
        email = signup_form.cleaned_data.get('email')
        password = signup_form.cleaned_data.get('password1')
        signup_form.save()
        return redirect('/')
    else:
        signup_form = SignUpForm()
    return render(request,'Todo_list/signup.html',{'form':signup_form})

def Login(request):
    if request.user.is_authenticated:
        return HttpResponse(f"{request.user} is already logged in.")
    login_form = LoginForm(request.POST or None)
    if login_form.is_valid():
        email = login_form.cleaned_data.get('email')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request,email = email, password = password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('home')
        else:
            return HttpResponse("Invalid Input!.Please enter your information correctly")
    else:
        login_form = LoginForm()
    return render(request,'Todo_list/login.html',{'form':login_form})

def Logout(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect('signup')

def Index(request):
    return render(request,'Todo_list/index.html')

def CreateTodo(request):
    context = {}
    todo_form = TodoForm(request.POST or None)
    if todo_form.is_valid():
        todo = todo_form.save()
        messages.success(request,"Successfully Created.")
        return redirect('home')
    context = {'form':todo_form}
    return render(request,'Todo_list/createtodo.html',context)

def TodoDetail(request,slug):
    context = {}
    todo = get_object_or_404(Todo,slug = slug)
    context = {'todo':todo}
    return render(request,'Todo_list/todo_detail.html',context)

def UpdateTodo(request,slug):
    context = {}
    todo = Todo.objects.filter(slug__iexact = slug)
    update_form = TodoForm(request.POST or None)
    if update_form.is_valid():
        update_form.save()
        messages.success(request,"Updated Successfully")
        return HttpResponseRedirect('todo_detail/'+ slug)
    context = {'form':update_form}
    return render(request,'Todo_list/update_todo.html',context)

    # after update: updated todo stores as another object in admin panel
    # todo before updated is also there in admin panel
    # error occured due to no instance is mentioned in TodoForm
    # while fetching data, if there is more than one todo with same slug;creates error







