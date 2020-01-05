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
    isFollowing = False

    ctx = dict()
    if request.method == "POST":
        user = request.user

        following_id = request.POST.get("id")
        if user.id is not following_id:
            following = get_object_or_404(User, pk=following_id)
            print(following.followers.all())
            if user.following.filter(pk=following_id).exists():
                isFollowing = False
                following.followers.remove(user)
                user.following.remove(following)
            else:
                isFollowing = True
                following.followers.add(user)
                user.following.add(following)
            print(user.following.all())
            print(user.followers.all())
            # following_list = user.following.values_list('id', flat=True)
            messages.info(request, message[isFollowing])
            ctx.update({"person": following, "isFollowing": isFollowing})

    # partial을 rendering 한 결과를 전송.
    html = render_to_string("partial/_user.html", ctx)
    msg = render_to_string("messages.html", {"messages":messages.get_messages(request)})
    ctx = {
        "target": f"{following.id}",
        "data": html,
        "msg": msg
    }
    return JsonResponse(ctx)


def profile(request):
    user = request.user
    following_list = user.following.all()
    follower_list = user.followers.all()

    print(following_list)
    print(follower_list)

    ctx = {
        'user': request.user,
        'following': following_list,
        'following_ids': following_list.values_list('id', flat=True),
        'followers': follower_list,
        'follower_ids': follower_list.values_list('id', flat=True),
    }
    return render(request, "profile.html", ctx)


def userListView(request):
    following_list = request.user.following.values_list('id', flat=True)
    ctx = {"users": User.objects.select_related("profile").all().exclude(id=request.user.id)}
    ctx.update({"following": list(following_list)})
    return render(request, "userList.html", ctx)


def logoutView(request):
    logout(request)
    return redirect('home')


def deleteUsers(request):
    users = User.objects.all()
    for user in users:
        if user.email != "root@root.com":
            user.delete()

    return redirect('home')
