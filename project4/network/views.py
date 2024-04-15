from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Post
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User


def index(request):
    posts = Post.objects.order_by("-date_edit_post")
    paginator = Paginator(posts,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "page_obj":page_obj
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
def addpost (request):
    if request.method == "POST":
        new_post = Post.objects.create(
            user = request.user,
            content = request.POST['content']
        )
    return HttpResponseRedirect(reverse("index"))

def user_page (request, user):
    page_user = User.objects.get(pk=user)
    posts = Post.objects.filter(user=user).order_by("-date_edit_post")
    paginator = Paginator(posts,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    user = User.objects.get(pk=request.user.id)
    if page_user in user.follow.all():
        follow_btn = 'Unfollow'
    else:
        follow_btn = 'Follow'
    return render (request, "network/user.html", {
        "page_obj": page_obj,
        "page_user": page_user,
        "follow_btn": follow_btn
    })

def following (request,user):
    user = User.objects.get(pk=user)
    my_follows = user.follow.all()
    return render (request, "network/following.html", {
        "my_follows": my_follows
    })


@csrf_exempt
@login_required
def edit (request, post):
    try:
        edit_post = Post.objects.get(user=request.user, pk=post)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Invalid operation"}, status=400)
    if request.method == "POST":
        data = json.loads(request.body)
        if data.get("content") is not None:
            edit_post.content = data["content"]
            edit_post.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "POST request required"
        }, status=400)
    
@csrf_exempt
@login_required
def like (request,post):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        like_post = Post.objects.get(pk=post)
        if user in like_post.likes.all():
            like_post.likes.remove(user)
        else: 
            like_post.likes.add(user)
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "POST request required"
        }, status=400)
    
@csrf_exempt
@login_required
def follow (request,user):
    if request.method == "POST":
        follower = User.objects.get(pk=request.user.id)
        user = User.objects.get(pk=user)
        followers = user.followers.all()
        if follower in followers:
            user.followers.remove(follower)
            follower.follow.remove(user)
        else: 
            user.followers.add(follower)
            follower.follow.add(user)
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "POST request required"
        }, status=400)
