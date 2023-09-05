from django.shortcuts import render, redirect, get_object_or_404
from authy.forms import SignupForm, ChangePasswordForm, EditProfileForm
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from authy.models import Profile
from notifications.models import Notification, Notification_StartUp

from post_StartUp.models import Post_StartUp
from post.models import Post, Follow, Stream

from django.db import transaction
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.core.paginator import Paginator

from django.urls import resolve
from authy.utils import *


# Create your views here.
def UserProfile(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	url_name = resolve(request.path).url_name

	# template = loader.get_template('base.html')
	
	if url_name == 'profile':
		posts = Post.objects.filter(user=user).order_by('-posted')
		posts_StartUp = Post_StartUp.objects.filter(user=user).order_by('-posted')

	else:
		posts = profile.favorites.all()
		posts_StartUp = profile.favorites_StartUp.all()

	#Profile info box
	posts_count = Post.objects.filter(user=user).count() 
	posts_StartUp_count = Post_StartUp.objects.filter(user=user).count() 
	psts_count=posts_count+posts_StartUp_count
	#favorite calculation
	favorites_count = profile.favorites.count()
	favorites_StartUp_count = profile.favorites_StartUp.count()
	fav_count=favorites_count+favorites_StartUp_count
	#favorite count
	following_count = Follow.objects.filter(follower=user).count()
	followers_count = Follow.objects.filter(following=user).count() 

	#follow status
	follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

	#notifications
	notifications = Notification.objects.filter(user=request.user).order_by('-date')[:3]
	notifications_all = Notification.objects.all().order_by('-date')[:3]
	Notification.objects.filter(user=request.user, is_seen=False).update(is_seen=True)

	#notifications startUp
	notifications_startUp = Notification_StartUp.objects.filter(user=request.user).order_by('-date')[:3]
	notifications_startUp_all = Notification_StartUp.objects.all().order_by('-date')[:3]
	Notification_StartUp.objects.filter(user=request.user, is_seen=False).update(is_seen=True)

	# user_SELF =request.user.id
	# posts_self  = Post.objects.filter(user=user_SELF).order_by('-posted')
	# posts_StartUp_self  = Post_StartUp.objects.filter(user=user_SELF).order_by('-posted')

	profileUser_post  = Post.objects.filter(user=profile.user).order_by('-posted')
	profileUser_post_StartUp  = Post_StartUp.objects.filter(user=profile.user).order_by('-posted')


	#Pagination
	#tech
	page_number = request.GET.get('page')
	paginator = Paginator(posts, 10)
	posts_paginator = paginator.get_page(page_number)
	#startUp
	paginator_StartUp = Paginator(posts_StartUp, 100)
	posts_paginator_StartUp = paginator_StartUp.get_page(page_number)


	template = loader.get_template('profile.html') 


	followingAndfollowers_number=[following_count, followers_count]
	followingAndfollowers_names=['following_count', 'followers_count']

	followingAndfollowers=get_bar_chart_profileDashboard_mentor_fellow(followingAndfollowers_names, followingAndfollowers_number)


	posts_value_unique_=[psts_count, fav_count]
	posts_names_unique_=['posts_count', 'favorites_count']

	sum_of_Experience_unique_count=get_bar_chart_profileDashboard_mentoring_learning(posts_names_unique_, posts_value_unique_)

	

	context = {
		'posts_StartUp':posts_paginator_StartUp,
		'posts': posts_paginator,

		# 'posts_self':posts_self,
		# 'posts_StartUp_self':posts_StartUp_self,

		'profileUser_post':profileUser_post,
		'profileUser_post_StartUp':profileUser_post_StartUp,
		
		'profile':profile,
		'following_count':following_count,
		'followers_count':followers_count,

		'psts_count':psts_count,
		'fav_count':fav_count,

		'follow_status':follow_status,
		'url_name':url_name,

		'notifications': notifications,
		'notifications_all':notifications_all,
		'notifications_startUp':notifications_startUp,
		'notifications_startUp_all':notifications_startUp_all,

		'followingAndfollowers':followingAndfollowers,
		'sum_of_Experience_unique_count':sum_of_Experience_unique_count,
	}

	return HttpResponse(template.render(context, request))


def profilefavorites(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	url_name = resolve(request.path).url_name
	
	posts = profile.favorites.all()
	posts_StartUp = profile.favorites_StartUp.all()

	#Profile info box
	posts_count = Post.objects.filter(user=user).count() 
	posts_StartUp_count = Post_StartUp.objects.filter(user=user).count() 
	psts_count=posts_count+posts_StartUp_count
	#favorite calculation
	favorites_count = profile.favorites.count()
	favorites_StartUp_count = profile.favorites_StartUp.count()
	fav_count=favorites_count+favorites_StartUp_count
	#following count
	following_count = Follow.objects.filter(follower=user).count()
	followers_count = Follow.objects.filter(following=user).count()

	#follow status
	follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

	#notifications
	notifications = Notification.objects.filter(user=request.user).order_by('-date')[:3]
	notifications_all = Notification.objects.all().order_by('-date')[:3]
	Notification.objects.filter(user=request.user, is_seen=False).update(is_seen=True)

	#notifications startUp
	notifications_startUp = Notification_StartUp.objects.filter(user=request.user).order_by('-date')[:3]
	notifications_startUp_all = Notification_StartUp.objects.all().order_by('-date')[:3]
	Notification_StartUp.objects.filter(user=request.user, is_seen=False).update(is_seen=True)

	#Pagination
	#tech
	page_number = request.GET.get('page')
	paginator = Paginator(posts, 10)
	posts_paginator = paginator.get_page(page_number)
	#startUp
	paginator_StartUp = Paginator(posts_StartUp, 100)
	posts_paginator_StartUp = paginator_StartUp.get_page(page_number)

	template = loader.get_template('profile_favorite.html')

	# user_SELF =request.user.id
	# posts_self  = Post.objects.filter(user=user_SELF).order_by('-posted')
	# posts_StartUp_self  = Post_StartUp.objects.filter(user=user_SELF).order_by('-posted')


	followingAndfollowers_number=[following_count, followers_count]
	followingAndfollowers_names=['following_count', 'followers_count']

	followingAndfollowers=get_bar_chart_profileDashboard_mentor_fellow(followingAndfollowers_names, followingAndfollowers_number)


	posts_value_unique_=[psts_count, fav_count]
	posts_names_unique_=['posts_count', 'favorites_count']

	sum_of_Experience_unique_count=get_bar_chart_profileDashboard_mentoring_learning(posts_names_unique_, posts_value_unique_)
	


	context = {
		'posts_StartUp':posts_paginator_StartUp,
		'posts': posts_paginator,

		# 'posts_self':posts_self,
		# 'posts_StartUp_self':posts_StartUp_self,

		'profile':profile,
		'following_count':following_count,
		'followers_count':followers_count,
		'psts_count':psts_count,
		'fav_count':fav_count,

		'follow_status':follow_status,
		'url_name':url_name,

		'notifications': notifications,
		'notifications_all':notifications_all,
		'notifications_startUp':notifications_startUp,
		'notifications_startUp_all':notifications_startUp_all,

		'followingAndfollowers':followingAndfollowers,
		'sum_of_Experience_unique_count':sum_of_Experience_unique_count,
	}

	return HttpResponse(template.render(context, request))


def Signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			User.objects.create_user(username=username, email=email, password=password)
			return redirect('index')
	else:
		form = SignupForm()
	
	context = {
		'form':form,
	}

	return render(request, 'signup.html', context)


@login_required
def PasswordChange(request):
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

	context = {
		'form':form,
	}

	return render(request, 'change_password.html', context)

def PasswordChangeDone(request):
	return render(request, 'change_password_done.html')


@login_required
def EditProfile(request):
	user = request.user.id
	profile = Profile.objects.get(user__id=user)
	BASE_WIDTH = 400

	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES)
		if form.is_valid():
			profile.picture = form.cleaned_data.get('picture')
			profile.first_name = form.cleaned_data.get('first_name')
			profile.last_name = form.cleaned_data.get('last_name')
			profile.location = form.cleaned_data.get('location')
			profile.githubProfile = form.cleaned_data.get('githubProfile')
			profile.linkedInnProfile = form.cleaned_data.get('linkedInnProfile') 
			profile.interstCategory = form.cleaned_data.get('interstCategory')
			profile.save()
			return redirect('index')
	else:
		form = EditProfileForm()

	#notifications
	notifications = Notification.objects.filter(user=request.user).order_by('-date')[:3]
	notifications_all = Notification.objects.all().order_by('-date')[:3]
	Notification.objects.filter(user=request.user, is_seen=False).update(is_seen=True)

	#notifications startUp
	notifications_startUp = Notification_StartUp.objects.filter(user=request.user).order_by('-date')[:3]
	notifications_startUp_all = Notification_StartUp.objects.all().order_by('-date')[:3]
	Notification_StartUp.objects.filter(user=request.user, is_seen=False).update(is_seen=True)


	user_SELF =request.user.id
	posts_self  = Post.objects.filter(user=user_SELF).order_by('-posted')


	context = {
		'form':form,
		
		'notifications': notifications,
		'notifications_all':notifications_all,
		'notifications_startUp':notifications_startUp,
		'notifications_startUp_all':notifications_startUp_all,

		'posts_self':posts_self,
	}

	return render(request, 'edit_profile.html', context)


@login_required
def follow(request, username, option):
	following = get_object_or_404(User, username=username)

	try:
		f, created = Follow.objects.get_or_create(follower=request.user, following=following)

		if int(option) == 0:
			f.delete()
			Stream.objects.filter(following=following, user=request.user).all().delete()
		else:
			 posts = Post.objects.all().filter(user=following)[:25]

			 with transaction.atomic():
			 	for post in posts:
			 		stream = Stream(post=post, user=request.user, date=post.posted, following=following)
			 		stream.save()

		return HttpResponseRedirect(reverse('profile', args=[username]))
	except User.DoesNotExist:
		return HttpResponseRedirect(reverse('profile', args=[username]))



def DeleteNotification(request, noti_id):
	user = request.user
	Notification.objects.filter(id=noti_id, user=user).delete()
	return redirect('index')


def CountNotifications(request):
	count_notifications = 0
	if request.user.is_authenticated:
		count_notifications = Notification.objects.filter(user=request.user, is_seen=False).count()

	return {'count_notifications':count_notifications}
	



##########################################################################################################################################################################################

@login_required
def Delete_account(request):

	if request.user == request.user:
		delete_user = User.objects.get(username=request.user)
		delete_user.delete()
		return redirect('signup')
	else:
		return redirect('signup')

##########################################################################################################################################################################################

@login_required
def pre_Delete_account(request):
	# if request.method == 'POST':
	if request.user == request.user:
		delete_user = User.objects.get(username=request.user)
		context={'delete_user':delete_user}
		return render(request, 'pre_Delete_account.html', context)		
	else:
		return redirect('signup')		
