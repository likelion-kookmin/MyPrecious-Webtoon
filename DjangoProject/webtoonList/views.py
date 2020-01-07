from django.shortcuts import render, redirect
from django.db.models import Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt

import random

from contentsApp.models import *
from accountApp.models import Profile


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
    profile = Profile.objects.get(user__id=request.user.id)
    subscribe_webtoons = profile.subscribes.all().order_by("id")
    print(subscribe_webtoons)
    paginator = Paginator(subscribe_webtoons, 5)
    page = request.GET.get('page')
    try:
        wts = paginator.get_page(page)
    except PageNotAnInteger:
        wts = paginator.get_page(1)
    except EmptyPage:
        wts = Paginator.get_page(paginator.num_pages)
    return render(request, "webtoon_list.html", {"title": "구독한 웹툰들", "webtoons": wts})


def Random(request):
    per_page = 5
    webtoons = get_random_webtoon(per_page)
    # 시간 테스트
    # import timeit
    # print(timeit.timeit(get_random_webtoon, number=100))
    return render(request, "webtoon_list.html", {"title": "구독한 웹툰들", "webtoons": webtoons})


def get_random_webtoon(number_of_webtoons=1):
    max_id = Webtoon.objects.all().aggregate(max_id=Max("id"))['max_id']

    # 뽑고자 하는 갯수보다 적거나, max_id가 뽑고 싶은 갯수보다 적을 경우
    if max_id <= number_of_webtoons:
        return Webtoon.objects.all()

    webtoon_list = set()
    while len(webtoon_list) < number_of_webtoons:
        pk = random.randint(1, max_id)
        webtoon = Webtoon.objects.get(pk=pk)
        webtoon_list.add(webtoon)

    return webtoon_list
