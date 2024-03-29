from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.template.loader import render_to_string

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
    search_word = request.GET.get("keyword")
    wts_search = Webtoon.objects.all()

    by_name = wts_search.filter(name__icontains=search_word)
    by_cartoonists = wts_search.filter(cartoonists__name=search_word)

    paginator = Paginator(by_name, 5)
    page = request.GET.get('page')
    try:
        wts_search_by_name = paginator.get_page(page)
    except PageNotAnInteger:
        wts_search_by_name = paginator.get_page(1)
    except EmptyPage:
        wts_search_by_name = Paginator.get_page(paginator.num_pages)

    paginator1 = Paginator(by_cartoonists, 5)
    page = request.GET.get('page')
    try:
        wts_search_by_cartoonists = paginator1.get_page(page)
    except PageNotAnInteger:
        wts_search_by_cartoonists = paginator1.get_page(1)
    except EmptyPage:
        wts_search_by_cartoonists = Paginator1.get_page(paginator1.num_pages)
    return render(request, "search_list.html", {"search_word": search_word, "wts_search_by_name": wts_search_by_name,
                                                "wts_search_by_cartoonists": wts_search_by_cartoonists})


def subscribe_list(request):
    profile = Profile.objects.get(user__id=request.user.id)
    subscribe_webtoons = profile.subscribes.all().order_by("id")
    subscribe_webtoon_ids = subscribe_webtoons.values_list("id", flat=True)

    paginator = Paginator(subscribe_webtoons, 5)
    page = request.GET.get('page')
    try:
        wts = paginator.get_page(page)
    except PageNotAnInteger:
        wts = paginator.get_page(1)
    except EmptyPage:
        wts = Paginator.get_page(paginator.num_pages)
    return render(request, "webtoon_list.html",
                  {"title": "구독한 웹툰들", "webtoons": wts, "checkList": subscribe_webtoon_ids})


def subscribe(request):
    message = ("unsubscribe", "subscribe",)

    ctx = dict()
    if request.method == "POST":
        user = request.user
        subscribes = user.profile.subscribes

        webtoon_id = request.POST.get("id")
        print(webtoon_id)
        webtoon = get_object_or_404(Webtoon, pk=webtoon_id)

        isSubscribed = subscribes.filter(pk=webtoon_id).exists()
        if isSubscribed:
            subscribes.remove(webtoon)
        else:
            subscribes.add(webtoon)

        # 구독이 되어있었다면 취소, 안되어 있었다면 구독
        messages.info(request, message[not isSubscribed])
        ctx.update({"webtoon": webtoon, "isSubscribed": not isSubscribed})
        html = render_to_string("partial/_webtoon.html", ctx)
        msg = render_to_string("messages.html", {"messages": messages.get_messages(request)})
        ctx = {
            "target": f"{ctx['webtoon'].id}",
            "data": html,
            "msg": msg
        }
        print(ctx)
    return JsonResponse(ctx)


def Random(request):
    per_page = 5
    webtoons = get_random_webtoon(per_page)
    subscribes = request.user.profile.subscribes.values_list("id", flat=True)

    # 시간 테스트
    # import timeit
    # print(timeit.timeit(get_random_webtoon, number=100))
    return render(request, "webtoon_list.html", {"title": "구독한 웹툰들", "webtoons": webtoons, "checkList":subscribes})


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
