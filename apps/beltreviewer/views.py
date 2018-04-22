# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

# Create your views here.
def index(request):

	return render(request, "beltreviewer/index.html")

def register(request):
	check = User.objects.register(
		request.POST["name"],
		request.POST["alias"],
		request.POST["email"],
		request.POST["password"],
		request.POST["confirm"]
	)

	if not check["valid"]:
		for error in check["errors"]:
			messages.add_message(request, messages.ERROR, error)
		return redirect("/")
	else:
		request.session["user_id"] = check["user"].id
		messages.add_message(request, messages.SUCCESS, "Welcome to Dojo Fitness, {}".format(request.POST["alias"]))
		return redirect("/books")

	

def login(request):
	check = User.objects.login(
        request.POST["email"],
        request.POST["password"]
    )

	if not check["valid"]:
		for error in check["errors"]:
			messages.add_message(request, messages.ERROR, error)
		return redirect("/")
	else:
		request.session["user_id"] = check["user"].id
		messages.add_message(request, messages.SUCCESS, "Welcome back, {}".format(check["user"].alias))
		return redirect("/books")


def books(request):
	user = User.objects.get(id=request.session["user_id"])
	other_review= Review.objects.all().exclude(user_id=request.session["user_id"]).order_by("-start")
	

	data= {
		"user":user,
		"other_review": other_review[:3]
	}

	return render(request, "beltreviewer/books.html", data)
	      

def logout(request):
    request.session.clear()
    messages.add_message(request, messages.SUCCESS, "See you later")
    return redirect("/")	      



