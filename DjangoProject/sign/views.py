from django.shortcuts import render, redirect
from .froms import UserForm
from dajngo.contrib.auth.models import User
from django.contrib.auth import login, authenticates
from django.template import RequestContext

# Create your views here.

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**from.cleaned_data)
            login(request, new_user)
            #임시 홈, 회원가입 성공 확인
            return render(request, 'thome.html')
    
    #나중에 오류메세지 구현하고 따로 구현하자
    #else:
        #form = UserForm()

def signin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        id = request.POST['id']
        ps = request.POST['ps']
        user = authenticates(id = id, ps = ps)

        if user is not None:
            login(request, user)
            #임시 홈, 로그인 성공 확인
            return render(request, 'thome.html')
        else:
            return HttpResponse('로그인 실패')
    
    #나중에 오류메세지 구현하고 따로 구현하자
    #else:
        #form = UserForm()

