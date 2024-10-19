from django.shortcuts import render, redirect, get_object_or_404
from authy.forms import SignupForm, ChangePasswordForm, EditProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, authenticate, login
from authy.models import Profile
from post.models import Post, Follow, Stream
from notifications.models import Notification
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib import messages

# Utility functions
def get_user_profile_data(user):
    profile = Profile.objects.get(user=user)
    posts_count = Post.objects.filter(user=user).count()
    followers_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    return profile, posts_count, followers_count, following_count

def get_notifications(user):
    notifications = Notification.objects.filter(user=user).order_by('-date')[:50]
    Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)
    return notifications

def render_with_context(request, template_name, context):
    return render(request, template_name, context)

def get_paginated_posts(queryset, request):
    paginator = Paginator(queryset, 8)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)

# Views
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile, posts_count, followers_count, following_count = get_user_profile_data(user)
    posts = Post.objects.filter(user=user).order_by('-posted') if request.resolver_match.url_name == 'profile' else profile.favorites.all()
    
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()
    notifications = get_notifications(request.user)

    context = {
        'posts': get_paginated_posts(posts, request),
        'profile': profile,
        'following_count': following_count,
        'followers_count': followers_count,
        'posts_count': posts_count,
        'posts_favorites_count': profile.favorites.count(),
        'follow_status': follow_status,
        'notifications': notifications,
    }
    
    return render_with_context(request, 'profile.html', context)

def profile_saved(request, username):
    user = get_object_or_404(User, username=username)
    profile, posts_count, followers_count, following_count = get_user_profile_data(user)
    
    posts = profile.favorites.all()
    context = {
        'posts': get_paginated_posts(posts, request),
        'profile': profile,
        'following_count': following_count,
        'followers_count': followers_count,
        'posts_count': posts_count,
        'posts_favorites_count': profile.favorites.count(),
    }

    return render_with_context(request, 'profile_favorite.html', context)

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('stream')
        else:
            messages.error(request, 'Invalid username or password')

    post_items = Post.objects.all().order_by('-posted')[:5]
    context = {'post_items': post_items}

    return render_with_context(request, 'login.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('stream')
    else:
        form = SignupForm()

    post_items = Post.objects.all().order_by('-posted')[:5]
    context = {
        'post_items': post_items,
        'form': form,
    }

    return render_with_context(request, 'signup.html', context)

@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('change_password_done')
    else:
        form = ChangePasswordForm(instance=user)

    return render_with_context(request, 'change_password.html', {'form': form})

def password_change_done(request):
    return render_with_context(request, 'change_password_done.html', {})

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            for field in ['picture', 'first_name', 'last_name', 'location', 'url_linkedInn', 'url_github', 'profile_info']:
                setattr(profile, field, form.cleaned_data.get(field))
            profile.save()
            return redirect('stream')
    else:
        form = EditProfileForm()

    notifications = get_notifications(request.user)
    context = {
        'form': form,
        'notifications': notifications,
    }

    return render_with_context(request, 'edit_profile.html', context)

@login_required
def mentoring_follow(request, username, option):
    following = get_object_or_404(User, username=username)
    try:
        follow_obj, created = Follow.objects.get_or_create(follower=request.user, following=following)

        if int(option) == 0:
            follow_obj.delete()
            Stream.objects.filter(following=following, user=request.user).delete()
        else:
            posts = Post.objects.filter(user=following)[:25]
            with transaction.atomic():
                Stream.objects.bulk_create(Stream(post=post, user=request.user, date=post.posted, following=following) for post in posts)

        return HttpResponseRedirect(reverse('profile', args=[username]))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args=[username]))
