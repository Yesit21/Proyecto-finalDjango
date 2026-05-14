from django.shortcuts import redirect, render
from django.urls import reverse


def home(request):
    if not request.user.is_authenticated:
        return redirect(reverse("usuarios:login"))
    return render(request, "dashboard/home.html")
