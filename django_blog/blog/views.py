from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import views as auth_views
from .forms import Cust_User_CreationForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required

#CRUD Operations
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment #Comments
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PostForm, CommentForm
from django.db.models import Q #Q objects to filter posts based on their title, content, or tags.

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = Cust_User_CreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) #Authomatically log in the user
            return redirect('Profile')
        else:
            form = Cust_User_CreationForm()
            return render(request, 'blog/register.html', {'form': form})
        
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'blog/profile.html', {'form': form})

#CRUD Operations
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/posts/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
#Comment MOdel view
@login_required
def CommentCreateView(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form, 'post': post})

@login_required
def CommentUpdateView(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/edit_comment.html', {'form': form, 'comment': comment})

@login_required
def CommentDeleteView(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    if request.method == 'POST':
        comment.delete()
        return redirect('post_detail', pk=comment.post.pk)
    return render(request, 'blog/delete_comment.html', {'comment': comment})

def search_posts(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) | 
            Q(tags__name__icontains=query)
        ).distinct()
    else:
        posts = Post.objects.all()
    
    return render(request, 'blog/search_results.html', {'posts': posts})

class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/post_list_by_tag.html'  # The template for displaying posts by tag
    context_object_name = 'posts'

    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name')
        return Post.objects.filter(tags__name__icontains=tag_name)