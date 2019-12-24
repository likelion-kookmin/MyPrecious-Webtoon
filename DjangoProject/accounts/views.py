from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SingupForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.template import RequestContext


# Create your views here.
def signup(request):
    if request.method == "POST":
        form = SingupForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect("home")

    form = SingupForm()
    ctx = {
        'form': form
    }
    return render(request, 'signup.html', ctx)


def login(request):
    ctx = dict()
    if request.method == "POST":
        form = LoginForm(request.POST)
        # clean에 정의된 대로 user_id를 저장한다.
        if form.is_valid():
            # 저장된 user를 세션의 user에 저장한다.
            request.session['user'] = form.user_id
            return redirect("home")

    form = LoginForm()
    ctx = {
        'form': form
    }
    return render(request, 'login.html', ctx)
