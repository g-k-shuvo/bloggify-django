from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Topic, Post, Comment
from .forms import PostCreateForm, PostEditForm, CommentForm


def home(request):
    featured_posts = []
    topics = Topic.objects.all()
    for topic in topics:
        featured_posts.append(topic.post_set.latest('-date'))
    recent_posts = Post.objects.all().order_by('-date')[:6]
    context = {
        'featured_posts': featured_posts,
        'recent_posts': recent_posts
    }
    return render(request, 'blog/home.html', context)

def blog(request):
    posts = Post.objects.all().order_by('-date')
    paginator = Paginator(posts, 9)
    page = request.GET.get('page')
    all_posts = paginator.get_page(page)
    context = {
        'all_posts': all_posts,
    }
    return render(request, 'blog/blog.html', context)

def topic(request, name):
    topic_posts = Post.objects.all().filter(topic__name=name)
    context = {
        'topic_posts': topic_posts,
        'topic_name': name,
    }
    return render(request, 'blog/topic.html', context)

def detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    similar_posts = Post.objects.filter(topic=post.topic).exclude(id=post.id)[:3]
    topics = Topic.objects.all()
    topic_post_count = Topic.objects.annotate(num_of_posts=Count('post'))
    topic_post_zipped = zip(topics, topic_post_count)
    total_likes = post.likes.count
    liked = False
    total_comments = Comment.objects.filter(post=post).count()
    comments = Comment.objects.all().filter(post=post)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('detail', pk)
    if post.likes.filter(pk=request.user.id).exists():
        liked = True
    context = {
        'post': post,
        'similar_posts': similar_posts,
        'topics': topics,
        'topic_post_zipped': topic_post_zipped,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'liked': liked,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'blog/detail.html', context)

def like(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_like'))
    liked = False
    if post.likes.filter(pk=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('detail', args=[str(pk)]))

def search(request):
    query = request.GET.get('query')
    search_results = Post.objects.filter(title__contains=query)
    context = {
        'query': query,
        'search_results': search_results
    } 
    return render(request, 'blog/search.html', context)

def author(request, username):
    author = User.objects.get(username=username)
    author_posts = Post.objects.filter(author=author).order_by('-date')
    context = {
        'author': author,
        'author_posts': author_posts
    } 
    if (author == request.user):
        return redirect('profile')
    else:
        return render(request, 'blog/author.html', context)

def create(request):
    if request.method == 'POST':
        post_create_form = PostCreateForm(request.POST, request.FILES) 
        if post_create_form.is_valid():
            post = post_create_form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('detail', args=[post.id]))
    else:
        post_create_form = PostCreateForm()
    context = {
        'post_create_form': post_create_form
    }

    return render(request, 'blog/create.html', context)

def edit(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        post_edit_form = PostEditForm(request.POST, request.FILES, instance=post)
        if post_edit_form.is_valid():
            post_edit_form.save()
            messages.success(request, 'Post has been updated!')
            return HttpResponseRedirect(reverse('detail', args=[str(pk)]))
    else:
        post_edit_form = PostEditForm(instance=post)
    context = {
        'post': post,
        'post_edit_form': post_edit_form
    }
    return render(request, 'blog/edit.html', context)

def delete(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == "POST":
        post.delete()
        messages.success(request, 'Post has been deleted!')
        return redirect('profile')
    context = {
        'post': post
    }
    return render(request, 'blog/delete.html', context)

