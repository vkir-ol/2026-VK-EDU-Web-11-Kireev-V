from django.shortcuts import render

AUTH_USER = {
    "nickname": "Ronny Cris",
    "login": "ronny_cris",
    "email": "ronny.cris@example.com",
    "avatar": "core/img/avatar-1.png",
}


def login(request):
    return render(request, "core/login.html")


def signup(request):
    return render(request, "core/signup.html")


def profile(request):
    return render(request, "core/profile.html", {"auth_user": AUTH_USER})
