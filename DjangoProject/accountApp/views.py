from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SingupForm, LoginForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout
from django.template import RequestContext


User = get_user_model()


# Create your views here.
def signupView(request):
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


def loginView(request):
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


def logoutView(request):
    logout(request)
    return redirect('home')