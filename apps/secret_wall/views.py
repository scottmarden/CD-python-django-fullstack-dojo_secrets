# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import User, Secret
import datetime


# Create your views here.
#-------------------------------Login, Registration & Logout--------------------------
def index(request):
	if 'user_id' in request.session:
		return redirect('/success')
	return render(request, 'secret_wall/index.html')

def register(request):
	result = User.objects.register(request.POST)
	if isinstance(result, list):
		for err in result:
			messages.add_message(request, messages.ERROR, err)
		return redirect('/')
	else:
		request.session['user_id'] = result.id
		return redirect('/success')

def login(request):
	result = User.objects.login(request.POST)
	if isinstance(result, list):
		for err in result:
			messages.add_message(request, messages.ERROR, err)
		return redirect('/')
	else:
		request.session['user_id'] = result.id
		return redirect('/success')

def logout(request):
	request.session.flush()
	return redirect('/')
#------------------------------------Homepage--------------------------------------
def success(request):
	if 'user_id' not in request.session:
		return redirect('/')
	user = User.objects.get(id=request.session['user_id'])
	liked_secrets = Secret.objects.user_likes(request.session['user_id'])
	created_secrets = Secret.objects.created_secrets(request.session['user_id'])
	recent_secrets = Secret.objects.recent_secrets()
	context = {
		'username': user.first_name,
		'secrets': recent_secrets,
		'liked_secrets': liked_secrets,
		'created_secrets': created_secrets,
	}
	return render(request, 'secret_wall/secrets.html', context)

def new_secret(request):
	user = User.objects.get(id=request.session['user_id'])
	result = Secret.objects.post(request.POST.get('new_secret'), user)
	if isinstance(result, str):
		print "GOT ERROR!"
		messages.add_message(request, messages.ERROR, result)
	return redirect('/success')

def like(request):
	result = Secret.objects.new_like(request.POST['secret_id'], request.session['user_id'])
	print result
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#------------------------------------Most Popular Page-------------------------------
def most_popular(request):
	if 'user_id' not in request.session:
		return redirect('/')
	user = User.objects.get(id=request.session['user_id'])
	result = Secret.objects.secrets_rank()
	liked_secrets = Secret.objects.user_likes(request.session['user_id'])
	created_secrets = Secret.objects.created_secrets(request.session['user_id'])
	context = {
		'username': user.first_name,
		'secrets': result,
		'liked_secrets': liked_secrets,
		'created_secrets': created_secrets,
	}
	return render(request, 'secret_wall/most_popular.html', context)

#------------------------------------Liked & Created by User Page-------------------------------
def known_secrets(request):
	if 'user_id' not in request.session:
		return redirect('/')
	user = User.objects.get(id=request.session['user_id'])
	liked_secrets = Secret.objects.user_likes(request.session['user_id'])
	created_secrets = Secret.objects.created_secrets(request.session['user_id'])
	context = {
		'username': user.first_name,
		'liked_secrets': liked_secrets,
		'created_secrets': created_secrets,
	}
	return render(request, 'secret_wall/known_secrets.html', context)

#--------------------------Neither Liked nor Created by User Page-------------------------------
def unknown_secrets(request):
	if 'user_id' not in request.session:
		return redirect('/')
	user = User.objects.get(id=request.session['user_id'])
	result = Secret.objects.unknown_secrets(request.session['user_id'])
	liked_secrets = Secret.objects.user_likes(request.session['user_id'])
	context = {
		'username': user.first_name,
		'secrets': result,
		'liked_secrets': liked_secrets,
	}
	return render(request, 'secret_wall/unknown_secrets.html', context)
