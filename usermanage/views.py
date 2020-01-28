from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
