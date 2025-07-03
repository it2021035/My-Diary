from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import logout,login
from django.contrib import messages
from posts.models import Post
from django.contrib.auth.decorators import login_required
# Create your views here.
def users_register(request):
    if request.method =="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request,form.save())
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect("posts:list")
    else:
        form = UserCreationForm()
    return render(request,'users/register.html',{"form":form})

def users_login(request): 
    if request.method == "POST": 
        form = AuthenticationForm(data=request.POST)
        if form.is_valid(): 
            login(request, form.get_user())
            messages.success(request, "Login successful.")
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("posts:list")
        else:
            messages.error(request, "Invalid username or password.")  
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", { "form": form })

def users_logout(request):
    if request.method =="POST":
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect("posts:list")
    else:
        form = AuthenticationForm()
    return render(request,'users/login.html',{"form":form})

@login_required(login_url="/users/login")
def users_dashboard(request):
    posts = Post.objects.filter(author=request.user).order_by("-date")
    return render(request, "users/dashboard.html", {"posts": posts})
