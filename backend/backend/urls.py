from django.contrib import admin
from django.urls import path
from .DSIP import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/post/create/", views.view_create_post),
    path("api/posts/get/", views.view_get_posts),
    path("api/posts_sv/get/", views.view_get_sv_posts),
    path("api/post/get/", views.view_get_post),
    path("api/post/update/body/", views.view_update_post_body),
    path("api/post/delete/", views.view_delete_post),
    path("api/post/vote/", views.view_vote_post),
    path("api/user/update/", views.view_delete_user_profile),
    path("api/set-session/", views.set_session),
    path("api/post/status", views.view_update_status_post),
    path("api/posts/get/user/upvoted/", views.view_get_user_liked_posts),
    path("api/posts/get/user/downvoted/", views.view_get_user_disliked_posts),
    path("api/posts/get/user/", views.view_get_user_posts),
    path("api/user/clear/", views.clear_session_cache),
    path("api/post/create/comment/", views.view_add_comment),
    path("api/post/delete/comment/", views.view_delete_comment),
]
