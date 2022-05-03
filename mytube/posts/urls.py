from django.urls import path

from . import views

urlpatterns = [
    # Подписки
    path("follow/", views.follow_index, name="follow_index"),
    path("<str:username>/follow/", views.profile_follow, name="profile_follow"),
    path("<str:username>/unfollow/", views.profile_unfollow, name="profile_unfollow"),
    # Главная страница
    path("", views.index, name="index"),
    # Добавление новой записи
    path("new/", views.new_post, name="new_post"),
    # Профайл пользователя
    path('<str:username>/', views.profile, name='profile'),
    # Группа
    path('group/<str:group_name>/', views.group_view, name='group'),
    # Просмотр записи
    path('<str:username>/<int:post_id>/', views.post_view, name='post'),
    path(
        '<str:username>/<int:post_id>/edit/',
        views.post_edit,
        name='post_edit'
    ),
    path("<username>/<int:post_id>/comment", views.add_comment, name="add_comment"),

]