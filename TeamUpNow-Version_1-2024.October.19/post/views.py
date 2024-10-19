from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from post.models import Stream, Post, Tag, Likes, Liked, Interested
from post.forms import NewPostForm
from notifications.models import Notification
from comment.models import Comment
from comment.forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from authy.models import Profile
from django.db.models import Count


# Helper function to fetch notifications
def get_notifications(user):
    notifications = Notification.objects.filter(user=user).order_by('-date')[:50]
    Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)
    return notifications


# Helper function to create or get tags
def get_or_create_tags(tags_form):
    tags_objs = []
    tags_list = list(tags_form.split(','))
    for tag in tags_list:
        t, _ = Tag.objects.get_or_create(title=tag.strip())
        tags_objs.append(t)
    return tags_objs


# Helper function to prepare context for templates
def prepare_context(request, extra_context=None):
    context = {
        'notifications': get_notifications(request.user),
        'notifications_all': Notification.objects.all().order_by('-date')[:50],
    }
    if extra_context:
        context.update(extra_context)
    return context


@login_required
def stream(request):
    user = request.user
    posts = Stream.objects.filter(user=user)
    
    # Fetch recent posts and top tags
    post_items = Post.objects.all().order_by('-posted')[:6]
    top_tags = Tag.objects.annotate(num_posts=Count('tags')).order_by('-num_posts')[:6]
    
    context = prepare_context(request, {
        'post_items': post_items,
        'top_tags': top_tags,
    })

    return render(request, 'stream.html', context)


@login_required
def post_details(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    profile = Profile.objects.get(user=user)
    favorited = profile.favorites.filter(id=post_id).exists()
    
    # Fetch comments
    comments = Comment.objects.filter(post=post).order_by('date')
    
    # Handle comment form submission
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            return HttpResponseRedirect(reverse('post_details', args=[post_id]))
    else:
        form = CommentForm()

    context = prepare_context(request, {
        'post': post,
        'favorited': favorited,
        'profile': profile,
        'form': form,
        'comments': comments,
        'liked': post.liked,
        'interested': post.interested,
    })

    return render(request, 'post_detail.html', context)


@login_required
def tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by('-posted')
    
    context = prepare_context(request, {
        'posts': posts,
        'tag': tag,
    })

    return render(request, 'tag.html', context)


@login_required
def like(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    liked = Likes.objects.filter(user=user, post=post).exists()

    # Update likes count
    if liked:
        Likes.objects.filter(user=user, post=post).delete()
        post.likes -= 1
    else:
        Likes.objects.create(user=user, post=post)
        post.likes += 1

    post.save()
    return HttpResponseRedirect(reverse('post_details', args=[post_id]))


@login_required
def liked(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    liked = Liked.objects.filter(user=user, post=post).exists()

    # Update liked count
    if liked:
        Liked.objects.filter(user=user, post=post).delete()
        post.liked -= 1
    else:
        Liked.objects.create(user=user, post=post)
        post.liked += 1

    post.save()
    return HttpResponseRedirect(reverse('post_details', args=[post_id]))


@login_required
def interested(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    liked = Interested.objects.filter(user=user, post=post).exists()

    # Update interested count
    if liked:
        Interested.objects.filter(user=user, post=post).delete()
        post.interested -= 1
    else:
        Interested.objects.create(user=user, post=post)
        post.interested += 1

    post.save()
    return HttpResponseRedirect(reverse('post_details', args=[post_id]))


@login_required
def favorite(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    profile = Profile.objects.get(user=user)

    if profile.favorites.filter(id=post_id).exists():
        profile.favorites.remove(post)
    else:
        profile.favorites.add(post)

    return HttpResponseRedirect(reverse('post_details', args=[post_id]))


@login_required
def add_post(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            title_post = form.cleaned_data.get('title_post')
            url_sourceContent = form.cleaned_data.get('url_sourceContent')
            caption = form.cleaned_data.get('caption')
            tags_form = form.cleaned_data.get('tags')

            tags_objs = get_or_create_tags(tags_form)

            Post.objects.create(caption=caption, title_post=title_post, url_sourceContent=url_sourceContent, user=request.user).tags.set(tags_objs)
            return redirect('stream')
    else:
        form = NewPostForm()

    context = prepare_context(request, {
        'form': form,
    })

    return render(request, 'newpost.html', context)


@login_required
def edit_post(request, event_id):
    post_object = get_object_or_404(Post, pk=event_id)

    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES, instance=post_object)
        
        if form.is_valid():
            post_object.url_sourceContent = form.cleaned_data.get('url_sourceContent')
            post_object.caption = form.cleaned_data.get('caption')
            tags_objs = get_or_create_tags(form.cleaned_data.get('tags'))
            post_object.tags.set(tags_objs)
            post_object.save()
            return redirect('stream')
    else:
        form = NewPostForm(instance=post_object)

    context = prepare_context(request, {
        'form': form,
    })

    return render(request, 'editPost.html', context)


@login_required
def delete_post(request, event_id):
    post = get_object_or_404(Post, pk=event_id)
    if request.user == post.user:
        post.delete()
    return redirect('stream')


@login_required
def pre_delete_post(request, event_id):
    post = get_object_or_404(Post, pk=event_id)
    if request.user == post.user:
        context = {'post': post}
        return render(request, 'pre_DeletePost_post.html', context)
    return redirect('stream')
