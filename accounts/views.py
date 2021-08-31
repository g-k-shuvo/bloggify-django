from django.http import request
from django.shortcuts import redirect, render
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from blog.models import Post
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        if password == password1:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is being used!')
                    return redirect('register')
                else:
                    user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                    user.save()
                    messages.success(request, 'You are now registered and can log in!')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    return render(request, 'accounts/register.html')

@login_required
def update(request):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)
        
    context = {
        'user_update_form':user_update_form,
        'profile_update_form':profile_update_form
    }
    return render(request, 'accounts/update.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in!")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('login')
    return render(request, 'accounts/login.html')


@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, "You are now logged out!")
    return redirect('home')

@login_required
def profile(request):
    user = request.user
    user_posts = Post.objects.filter(author=user).order_by('-date')
    context = {
        'user': user,
        'user_posts': user_posts
    }
    return render(request, 'accounts/user.html', context)

