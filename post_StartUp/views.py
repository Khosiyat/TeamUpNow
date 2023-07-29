from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from post_StartUp.models import  Tag_StartUp, Instructed_StartUp, Illustrated_StartUp, Post_StartUp, PostFileContent_StartUp
from post.models import Stream, Post, Tag,  Instructed, Illustrated
from post_StartUp.forms import NewPostForm_StartUp
from post.forms import NewPostForm


from stories.models import Story, StoryStream
from notifications.models import Notification, Notification_StartUp

from comment.models import Comment, Comment_StartUp
from comment.forms import CommentForm, CommentForm_StartUp


from django.contrib.auth.decorators import login_required

from django.urls import reverse
from authy.models import Profile
from authy.utils import *


# Create your views here.
 
def PostDetails_StartUp(request, post_id):
	post = get_object_or_404(Post_StartUp, id=post_id)
	user = request.user
	profile = Profile.objects.get(user=user)
	favorited = False

	#comment
	comments = Comment_StartUp.objects.filter(post=post).order_by('date')
	
	if request.user.is_authenticated:
		profile = Profile.objects.get(user=user) 

		if profile.favorites_StartUp.filter(id=post_id).exists():
			favorited = True

	#Comments Form
	if request.method == 'POST':
		form = CommentForm_StartUp(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.user = user
			comment.save()
			return HttpResponseRedirect(reverse('postdetails_StartUp', args=[post_id]))
	else:
		form = CommentForm_StartUp()

	#notifications
	notifications = Notification.objects.filter(user=request.user).order_by('-date')[:3]
	notifications_all = Notification.objects.all().order_by('-date')[:3]
	Notification.objects.filter(user=request.user, is_seen=False).update(is_seen=True)

	#notifications startUp
	notifications_startUp = Notification_StartUp.objects.filter(user=request.user).order_by('-date')[:3]
	notifications_startUp_all = Notification_StartUp.objects.all().order_by('-date')[:3]
	Notification_StartUp.objects.filter(user=request.user, is_seen=False).update(is_seen=True)
	
	user_SELF =request.user.id
	posts_self  = Post_StartUp.objects.filter(user=user_SELF).order_by('-posted')


	illustrated = post.illustrated
	instructed = post.instructed
	sumScore=illustrated+instructed


	posts_value_unique_=[illustrated, instructed]
	posts_names_unique_=['illustrated','instructed']
 
	contentQuality_score=get_pie_profileDashboard_projects(posts_value_unique_, posts_names_unique_)


	template = loader.get_template('post_detail_StartUp.html')

	context = {
		'post':post,
		'posts_self':posts_self,
		'favorited':favorited,
		'profile':profile,
		'form':form,
		'comments':comments, 
		
		'notifications': notifications,
		'notifications_all':notifications_all,
		'notifications_startUp':notifications_startUp,
		'notifications_startUp_all':notifications_startUp_all,

		'illustrated':illustrated,
		'instructed':instructed,
		'sumScore':sumScore,
		'contentQuality_score':contentQuality_score,
		
	}

	return HttpResponse(template.render(context, request))
  
@login_required
def NewPost_StartUp(request):
	user = request.user
	tags_objs = []
	files_objs = []

	if request.method == 'POST':
		form = NewPostForm_StartUp(request.POST, request.FILES)
		if form.is_valid():
			files = request.FILES.getlist('content')
			lessonLink = form.cleaned_data.get('lessonLink')
			codeSourceOfTheProject = form.cleaned_data.get('codeSourceOfTheProject')
			classCategory = form.cleaned_data.get('classCategory')
			caption = form.cleaned_data.get('caption')
			tags_form = form.cleaned_data.get('tagsStartUp')
			authorOfTheVideo = form.cleaned_data.get('authorOfTheVideo')

			tags_list = list(tags_form.split(', '))

			for tag in tags_list:
				t, created = Tag_StartUp.objects.get_or_create(title=tag)
				tags_objs.append(t)

			for file in files:
				file_instance = PostFileContent_StartUp(file=file, user=user)
				file_instance.save()
				files_objs.append(file_instance)

			p, created = Post_StartUp.objects.get_or_create(caption=caption, lessonLink=lessonLink,codeSourceOfTheProject = codeSourceOfTheProject, classCategory=classCategory, authorOfTheVideo=authorOfTheVideo, user=user)
			p.tagsStartUp.set(tags_objs)
			p.content.set(files_objs)
			p.save()
			return redirect('index')
	else:
		form = NewPostForm_StartUp()

	#notifications
	notifications = Notification.objects.filter(user=request.user).order_by('-date')[:3]
	notifications_all = Notification.objects.all().order_by('-date')[:3]
	Notification.objects.filter(user=request.user, is_seen=False).update(is_seen=True)

	#notifications startUp
	notifications_startUp = Notification_StartUp.objects.filter(user=request.user).order_by('-date')[:3]
	notifications_startUp_all = Notification_StartUp.objects.all().order_by('-date')[:3]
	Notification_StartUp.objects.filter(user=request.user, is_seen=False).update(is_seen=True)


	user_SELF =request.user.id
	posts_self  = Post_StartUp.objects.filter(user=user_SELF).order_by('-posted')

	context = {
		'form':form,
		'notifications': notifications,
		'posts_self':posts_self,
		
		'notifications': notifications,
		'notifications_all':notifications_all,
		'notifications_startUp':notifications_startUp,
		'notifications_startUp_all':notifications_startUp_all,
	}

	return render(request, 'newpost_StartUp.html', context)


def tags_StartUp(request, tag_slug):
	tag = get_object_or_404(Tag_StartUp, slug=tag_slug)
	posts = Post_StartUp.objects.filter(tagsStartUp=tag).order_by('-posted')

	template = loader.get_template('tag_StartUp.html')

	
	user_SELF =request.user.id
	posts_self  = Post_StartUp.objects.filter(user=user_SELF).order_by('-posted')

	#notifications
	notifications = Notification_StartUp.objects.filter(user=request.user).order_by('-date')
	notifications_all = Notification_StartUp.objects.all().order_by('-date')[:10]
	Notification_StartUp.objects.filter(user=request.user, is_seen=False).update(is_seen=True)

	context = {
		'posts':posts,
		'posts_self':posts_self,
		'tag':tag,
		'notifications': notifications,
		'notifications_all':notifications_all,
	}

	return HttpResponse(template.render(context, request))


 
@login_required
def instructed_StartUp(request, post_id):
	user = request.user
	post = Post_StartUp.objects.get(id=post_id)
	current_likes = post.instructed
	liked = Instructed_StartUp.objects.filter(user=user, post=post).count()

	if not liked:
		like = Instructed_StartUp.objects.create(user=user, post=post)
		#like.save()
		current_likes = current_likes + 1

	else:
		Instructed_StartUp.objects.filter(user=user, post=post).delete()
		current_likes = current_likes - 1

	post.instructed = current_likes
	post.save()

	return HttpResponseRedirect(reverse('postdetails_StartUp', args=[post_id]))



@login_required
def illustrated_StartUp(request, post_id):
	user = request.user
	post = Post_StartUp.objects.get(id=post_id)
	current_likes = post.illustrated
	liked = Illustrated_StartUp.objects.filter(user=user, post=post).count()

	if not liked:
		like = Illustrated_StartUp.objects.create(user=user, post=post)
		#like.save()
		current_likes = current_likes + 1

	else:
		Illustrated_StartUp.objects.filter(user=user, post=post).delete()
		current_likes = current_likes - 1

	post.illustrated = current_likes
	post.save()

	return HttpResponseRedirect(reverse('postdetails_StartUp', args=[post_id]))
	
@login_required
def favorite_StartUp(request, post_id):
	user = request.user
	post = Post_StartUp.objects.get(id=post_id)
	profile = Profile.objects.get(user=user)

	if profile.favorites_StartUp.filter(id=post_id).exists():
		profile.favorites_StartUp.remove(post)

	else:
		profile.favorites_StartUp.add(post)

	return HttpResponseRedirect(reverse('postdetails_StartUp', args=[post_id]))


########################################################################################################################################################################################## DELETE POST

@login_required
def DeletePost_StartUp(request, event_id):
	post = Post_StartUp.objects.get(pk=event_id)
	if request.user == post.user:
		post.delete()
		return redirect('index')		
	else:
		return redirect('index')		


@login_required
def pre_DeletePost_StartUp(request, event_id):
	post = Post_StartUp.objects.get(pk=event_id)
	if request.user == post.user:
		# post.delete()
		context={'post':post}
		return render(request, 'pre_DeletePost_StartUp.html', context)		
	else:
		return redirect('index')		

########################################################################################################################################################################################## EDIT POST


  
@login_required
def EditPost_StartUp(request, event_id):

	user = request.user.id
	post_object = Post_StartUp.objects.get(pk=event_id)

	post=Post_StartUp.objects.all()
	
	user = request.user
	tags_objs = []
	files_objs = []
	
	if request.method == 'POST':
		form = NewPostForm_StartUp(request.POST, request.FILES)
		if form.is_valid():
			files = request.FILES.getlist('content')

			post_object.caption = form.cleaned_data.get('caption')
			post_object.lessonLink = form.cleaned_data.get('lessonLink')
			post_object.authorOfTheVideo = form.cleaned_data.get('authorOfTheVideo')
			post_object.codeSourceOfTheProject = form.cleaned_data.get('codeSourceOfTheProject')
			post_object.classCategory = form.cleaned_data.get('classCategory')
			
			
			
			tags_form = form.cleaned_data.get('tagsStartUp')

			tags_list = list(tags_form.split(','))

			for tag in tags_list:
				t, created = Tag_StartUp.objects.get_or_create(title=tag)
				tags_objs.append(t)

			for file in files:
				file_instance = PostFileContent_StartUp(file=file, user=user)
				file_instance.save()
				files_objs.append(file_instance)

			p, created = Post_StartUp.objects.get_or_create(caption=post_object.caption, 
															lessonLink=post_object.lessonLink, 
															codeSourceOfTheProject=post_object.codeSourceOfTheProject, 
															authorOfTheVideo=post_object.authorOfTheVideo, 
															classCategory=post_object.classCategory, 
															user=user)
			p.tagsStartUp.set(tags_objs)
			p.content.set(files_objs)
			p.save()
			return redirect('index')
	else:
		form = NewPostForm_StartUp()

	#notifications
	notifications = Notification.objects.filter(user=request.user).order_by('-date')[:3]
	notifications_all = Notification.objects.all().order_by('-date')[:3]
	Notification.objects.filter(user=request.user, is_seen=False).update(is_seen=True)

	#notifications startUp
	notifications_startUp = Notification_StartUp.objects.filter(user=request.user).order_by('-date')[:3]
	notifications_startUp_all = Notification_StartUp.objects.all().order_by('-date')[:3]
	Notification_StartUp.objects.filter(user=request.user, is_seen=False).update(is_seen=True)


	template = loader.get_template('editPost_StartUp.html')

	context = {
		'form':form,
		'notifications': notifications,
		'notifications_all':notifications_all,
		'notifications_startUp':notifications_startUp,
		'notifications_startUp_all':notifications_startUp_all,
	}

	return HttpResponse(template.render(context, request))
 