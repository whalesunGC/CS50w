from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


def index(request):
    context = Post.objects.all()
    return render(request, "network/index.html", {
        "context":context,
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

def profile(request, username):
    context=User.objects.get(username=username)
    posts = Post.objects.filter(user=User.objects.get(username=username))
    followers=User.objects.filter(following=User.objects.get(username=username)).count()
    following=User.objects.filter(follower=User.objects.get(username=username)).count()
    follower =User.objects.filter(follower=User.objects.get(username=request.user)).contains(context)
    return render(request, "network/profile.html",{
        "context":context,
        "posts":posts,
        "followers":followers,
        "following":following,
        "follower":follower,
    })

def post(request, post_id):
    context=Post.objects.get(id=post_id)
    return render(request, "network/post.html",{
        'context':context,
    })

@login_required
@require_POST
@csrf_exempt
def follow(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    user = request.user
    if user_to_follow in user.following.all():
        user.following.remove(user_to_follow)
        followed = False
    else:
        user.following.add(user_to_follow)
        followed = True
    return JsonResponse({'followed': followed})