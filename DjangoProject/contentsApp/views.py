from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

import random

from .models import Webtoon, Comment
from .forms import CommentForm
from accountApp.models import Profile

# Create your views here.
WEBTOON_PER_PAGE = 6


def webtoon_detail(request, id):
    webtoon = get_object_or_404(Webtoon, pk=id)
    comment_form = CommentForm()
    comments = webtoon.comments.all()
    return render(request, 'webtoon_detail.html', {'webtoon': webtoon, "comments": comments, "form": comment_form})


def comment_create(request, id):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        comment_form.instance.user_id = request.user.id
        comment_form.instance.webtoon_id = id
        if comment_form.is_valid():
            comment = comment_form.save()
    return redirect('contentsApp:detail', id)


def comment_delete(request, id):
    delete_comment = Comment.objects.get(pk=id)
    webtoon_id = delete_comment.webtoon.id
    delete_comment.delete()
    return redirect('contentsApp:detail', webtoon_id)


@csrf_exempt
@login_required
def Search(request):
    ctx = dict()

    page = request.GET.get('page')
    search_word = request.GET.get("keyword")
    search_type = request.GET.get('type')

    wts_search = Webtoon.objects.all().order_by("id")

    subscribed_webtoon_pk_list = get_subscribed_webtoon_pk_list(request.user)
    ctx.update({"checkList": subscribed_webtoon_pk_list})

    print(search_type)
    if search_type != "cartoonist":
        search_type = "name"
        by_name = wts_search.filter(name__icontains=search_word).order_by("id")
        webtoons = make_page(by_name, page, WEBTOON_PER_PAGE)
    else:
        search_type = "cartoonist"
        by_cartoonists = wts_search.filter(cartoonists__name=search_word).order_by("id")
        webtoons = make_page(by_cartoonists, page, WEBTOON_PER_PAGE)

    print(search_type)
    ctx.update({"search_word": search_word, "webtoons": webtoons, "type": search_type})
    return render(request, "webtoon_search_list.html", ctx)


@login_required
def subscribe_list(request):
    profile = Profile.objects.get(user__id=request.user.id)
    subscribe_webtoons = profile.subscribes.all().order_by("id")
    subscribe_webtoon_ids = subscribe_webtoons.values_list("id", flat=True)

    page = request.GET.get('page')
    wts = make_page(subscribe_webtoons, page, WEBTOON_PER_PAGE)

    return render(request, "webtoon_list.html",
                  {"title": "구독한 웹툰들", "webtoons": wts, "checkList": subscribe_webtoon_ids})


def subscribe(request):
    message = ("unsubscribe", "subscribe",)

    ctx = dict()
    if request.method == "POST":
        user = request.user
        subscribes = user.profile.subscribes
        subscribed_webtoon_pk_list = get_subscribed_webtoon_pk_list(user)

        webtoon_id = request.POST.get("id")
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
    return JsonResponse(ctx)


def Random(request):
    webtoons = get_random_webtoon(WEBTOON_PER_PAGE)
    subscribed_webtoon_list = get_subscribed_webtoon_pk_list(request.user)

    # 시간 테스트
    # import timeit
    # print(timeit.timeit(get_random_webtoon, number=100))
    return render(request, "webtoon_list.html",
                  {"title": "랜덤 웹툰들", "webtoons": webtoons, "checkList": subscribed_webtoon_list})


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


def tag_list(request):
    keyword = request.GET.get("keyword")
    by_tag = Webtoon.objects.all().order_by("id") \
        .filter(tags__tag_name=keyword)

    subscribed_webtoon_ids = get_subscribed_webtoon_pk_list(request.user)

    page = request.GET.get('page')
    webtoons = make_page(by_tag, page, WEBTOON_PER_PAGE)

    return render(request, "webtoon_list.html", {"title": keyword, "webtoons": webtoons, "keyword": keyword,
                                                 "checkList": subscribed_webtoon_ids})


def make_page(objects, page_number, per_page=WEBTOON_PER_PAGE):
    paginator = Paginator(objects, per_page)
    try:
        page = paginator.get_page(page_number)
    except PageNotAnInteger:
        page = paginator.get_page(1)
    except EmptyPage:
        page = paginator.get_page(paginator.num_pages)
    return page


def get_subscribed_webtoon_pk_list(user):
    try:
        profile = get_object_or_404(Profile, user=user)
        subscribe_webtoons = profile.subscribes
        subscribe_webtoon_ids = subscribe_webtoons.values_list("pk", flat=True)
        return subscribe_webtoon_ids
    except AttributeError:
        return []
