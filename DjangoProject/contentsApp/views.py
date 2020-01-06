from django.shortcuts import render
from .models import *
from contentsApp.models import *

# Create your views here.
def webtoon_detail(request, id):
    webtoon = Webtoon.objects.get(pk=id)
    return render(request, 'webtoon_detail.html', {'webtoon': webtoon})

def list_test(request):
    contents = Webtoon.objects.all()
    return render(request, 'list.html', {'contents': contents})