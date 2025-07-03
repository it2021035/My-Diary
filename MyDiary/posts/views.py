from django.shortcuts import render , redirect
from .models import Post
from django.contrib.auth.decorators import login_required
from . import forms
from django.shortcuts import get_object_or_404
    # Create your views here.


def posts_list(request):
    posts = Post.objects.all().order_by('-date')
    return render(request, 'posts/posts_list.html', {'posts': posts})

def post_page(request ,slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'posts/post_page.html', {'post': post})

@login_required(login_url="/users/login")
def post_new(request):
    if request.method =='POST':
        form = forms.CreatePost(request.POST, request.FILES)
        if form.is_valid():
            newpost = form.save(commit=False)
            newpost.author = request.user
            newpost.save() 
            return redirect('posts:list')
    else:    
        form = forms.CreatePost()
    return render(request, 'posts/post_new.html', {'form': form})

@login_required(login_url="/users/login")
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        return redirect('posts:page', slug=slug)
    
    if request.method == 'POST':
        form = forms.CreatePost(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:page', slug=post.slug)
    else:
        form = forms.CreatePost(instance=post)
    return render(request, 'posts/post_new.html', {'form': form, 'edit_mode': True})

@login_required(login_url="/users/login")
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        return redirect('posts:page', slug=slug)
    
    if request.method == 'POST':
        post.delete()
        return redirect('posts:list')
    
    return render(request, 'posts/confirm_delete.html', {'post': post})