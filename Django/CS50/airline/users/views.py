from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    return render(request, "users/index.html")


def login_view(request):
    if(request.method == "POST"):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("users:index"))
        else:
            return render(request, "users/login.html", {
                "message": "Invalid Credentials",
            })
    else:
        return render(request, "users/login.html")


def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
        "message": "User Logged Out"
    })