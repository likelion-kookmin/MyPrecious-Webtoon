from django.shortcuts import render, redirect
from contentsApp.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def Rated(request):
    return render(request, "random_list.html")


def Rating(request):
    return render(request, "random_list.html")


@csrf_exempt
def Search(request):
    search_word = request.POST.get('Search', '').strip()
    wts_search = Webtoon.objects.all()
    by_name = wts_search.filter(name__icontains=search_word)
    wts_search_by_cartoonists = wts_search.filter(cartoonists__name=search_word)
    paginator = Paginator(by_name, 5)
    page = request.POST.get('page')
    try:
        wts_search_by_name = paginator.get_page(page)
    except PageNotAnInteger:
        wts_search_by_name = paginator.get_page(1)
    except EmptyPage:
        wts_search_by_name = Paginator.get_page(paginator.num_pages)
    return render(request, "search_list.html", {"search_word": search_word, "wts_search_by_name": wts_search_by_name,
                                                "wts_search_by_cartoonists": wts_search_by_cartoonists})


def Subscribe(request):
    return render(request, "random_list.html")


def Random(request):
    webtoons = Webtoon.objects.all()
    paginator = Paginator(webtoons, 5)
    page = request.GET.get('page')
    try:
        wts = paginator.get_page(page)
    except PageNotAnInteger:
        wts = paginator.get_page(1)
    except EmptyPage:
        wts = Paginator.get_page(paginator.num_pages)
    return render(request, "random_list.html", {"wts": wts})
