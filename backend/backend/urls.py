from django.contrib import admin
from django.urls import path
from .DSIP import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sean/<str:text>/", views.sean_view),
    path("api/post/create/", views.view_create_post),
    path("api/posts/get/", views.view_get_posts),
    path("api/post/get/", views.view_get_post),
    path("api/post/update/<str:post_id>", views.view_update_post),
    path("api/post/delete/", views.view_delete_post),
    path("api/post/vote/", views.view_vote_post),
    path("", views.view_login_user),
    path("api/user/update/", views.view_delete_user_profile),
    path("api/set-session", views.set_session),
    path("api/post/status", views.view_update_status_post),
]
