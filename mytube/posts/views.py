from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page

from .forms import PostForm, CommentFrom
from .models import Post, Comment, Follow


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


@cache_page(20)
def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator}
    )


@login_required
def new_post(request):
        flag = 'Новая запись'
        error = ''
        if request.method == 'POST':
            form = PostForm(request.POST or None, files=request.FILES or None)
            if form.is_valid():
                text = request.POST['text']
                aut = request.user
                if request.POST['group'] != '':
                    group = Group(pk=request.POST['group'])
                else:
                    group = None
                if request.FILES == {}:
                    newpost = Post(text=text, author=aut, group=group)
                else:
                    newpost = Post(text=text, author=aut, group=group, image=request.FILES['images'])
                newpost.save()
                return redirect('index')
            else:
                error = "Добавлять можно только изображения!"
        else:
            form = PostForm(request.POST, files=request.FILES or None)
        data = {
            "form": form,
            "error": error,
            "flag": flag,
        }
        return render(request, "new.html", data)


@login_required
def profile(request, username):
    profile_name = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author__username=username).order_by('-pub_date').all()
    count = post_list.count()
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    if Follow.objects.filter(user=request.user, author=User.objects.get(username=username)).count() != 0:
        following = True
    else:
        following = False
    follower_in = Follow.objects.filter(user__username=username).count()
    follower_out = Follow.objects.filter(author__username=username).count()
    data = {
            'profile': profile_name,
            'page': page,
            'paginator': paginator,
            'count': count,
            'following': following,
            'follower_in': follower_in,
            'follower_out': follower_out,
            }
    return render(request, 'profile.html', data)


@login_required
def group_view(request, group_name):
    groupname = get_object_or_404(Group, name=group_name)
    post_list = Post.objects.filter(group__name=group_name).order_by('-pub_date').all()
    count = post_list.count()
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    data = {
            'group_name': groupname,
            'page': page,
            'paginator': paginator,
            'count': count
            }
    return render(request, 'group.html', data)


@login_required
def post_view(request, username, post_id):
    profile_name = User.objects.get(username=username)
    post_list = Post.objects.filter(author__username=username).all()
    count = post_list.count()
    post = post_list.get(pk=post_id)
    form_c = CommentFrom()     # использование формы комментария
    comments = Comment.objects.filter(post__id=post_id).order_by('-created').all()
    follower_in = Follow.objects.filter(user__username=username).count()
    follower_out = Follow.objects.filter(author__username=username).count()
    data = {
        'profile': profile_name,
        'count': count,
        'post': post,
        'form_c': form_c,
        'comments': comments,
        'follower_in': follower_in,
        'follower_out': follower_out,
    }
    return render(request, 'post.html', data)


@login_required
def post_edit(request, username, post_id):
    flag = "Редактирование записи"
    error = ''
    post = Post.objects.filter(author__username=username).all().get(pk=post_id)
    if request.user == post.author:
         if request.method == 'POST':
             form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
             if form.is_valid():
                post.save()
                return redirect("/"+username+"/"+str(post_id))
             else:
                error = "Используйте файл изображения"
         else:
            form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
            return render(request, 'new.html', {"form": form, "error": error, "flag": flag})
         return render(request, 'new.html', {"form": form, "error": error, "flag": flag})
    else:
        return redirect("/"+username+"/"+str(post_id))


@login_required
def add_comment(request, username, post_id):
    post = Post.objects.get(pk=post_id)
    author = request.user
    text = request.POST['text']
    new_comment = Comment(post=post, author=author, text=text)
    new_comment.save()
    return redirect("/"+username+"/"+str(post_id))


# показывает посты на которые подписан человек
@login_required
def follow_index(request):
    # информация о текущем пользователе доступна в переменной request.user
    auth_list = Follow.objects.filter(user=request.user).all()
    post_list = Post.objects.none()
    for auth in auth_list:
        post_auth = Post.objects.filter(author=auth.author).all()
        post_list = post_list.union(post_auth, post_list)
    post_list = post_list.order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "follow.html", {'page': page, 'paginator': paginator})


# подписывается на человека
@login_required
def profile_follow(request, username):
    Follow.objects.create(user=request.user, author=User.objects.get(username=username))
    return redirect("/"+username+"/")


# отписывается от человека
@login_required
def profile_unfollow(request, username):
    Follow.objects.filter(user=request.user, author=User.objects.get(username=username)).delete()
    return redirect("/"+username+"/")


