import django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout
from django.template.loader import render_to_string

User = get_user_model()


# Create your views here.
def follow(request):
    message = ("unfollow", "follow",)

    ctx = dict()
    if request.method == "POST":
        user = request.user

        following_id = request.POST.get("id")
        target = get_object_or_404(User, pk=following_id)

        isFollowing = user.follow(target)
        messages.info(request, message[isFollowing])
        ctx.update({"person": target, "isFollowing": isFollowing})

        # partial을 rendering 한 결과를 전송.
        html = render_to_string("partial/_user.html", ctx)
        msg = render_to_string("messages.html", {"messages": messages.get_messages(request)})
        ctx = {
            "target": f"{ctx['person'].id}",
            "data": html,
            "msg": msg
        }
    return JsonResponse(ctx)


def profile(request):
    user = request.user
    follower_list = user.followers
    ctx = {
        'user': request.user,
        'people': follower_list,
        'checkList': user.following.values_list('id', flat=True),
    }
    return render(request, "profile.html", ctx)


def userListView(request):
    following_list = request.user.following.values_list('id', flat=True)
    ctx = {"users": User.objects.select_related("profile").all().exclude(id=request.user.id)}
    ctx.update({"following": list(following_list),
                "title": "추천 유저 목록"})
    return render(request, "userList.html", ctx)


def followListView(request):
    ctx = dict()
    type = request.GET.get("type").lower()
    following = request.user.following
    if type != "following":
        followers = request.user.followers
        ctx.update({"title": "follower 유저 목록",
                    "people": followers,
                    "checkList": following.values_list("id", flat=True)})
    else:
        ctx.update({"title": "following 유저 목록",
                    "people": following,
                    "checkList": following.values_list("id", flat=True)})

    html = render_to_string("partial/_userList.html", ctx)
    # msg = render_to_string("messages.html", {"messages": messages.get_messages(request)})
    print(ctx)
    ctx = {
        "target": "userList",
        "data": html
    }

    return JsonResponse(ctx)


def logoutView(request):
    logout(request)
    return redirect('home')


def deleteUsers(request):
    users = User.objects.all()
    for user in users:
        if user.email != "root@root.com":
            user.delete()

    return redirect('home')
