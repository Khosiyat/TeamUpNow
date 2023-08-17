from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages 

from django.shortcuts import render, redirect
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from django.db.models import Q
from django.core.paginator import Paginator

from datetime import date, timedelta,datetime


from django.conf import settings
from django.http import HttpResponseRedirect


def teamUpNowTech_login(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('index')
		else:
			messages.success(request, ("There Was An Error Logging In, Try Again..."))	
			return redirect('teamupnow.tech')	
	else:
		return render(request, 'teamUpNowTech_login.html', {})


def teamUpNowTech(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('index')
		else:
			messages.success(request, ("There Was An Error Logging In, Try Again..."))	
			return redirect('teamupnow.tech')	
	else:
		return render(request, 'teamUpNowTech.html', {})
