from django.contrib import admin
from django.urls import path
from .DSIP import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sean/<str:text>/", views.sean_view),
    path("api/admin/delete/<str:post_id>/", views.view_delete_user_post),
    path("api/admin/comment/<str:post_id>/", views.view_comment_as_admin),
    path("api/external", views.view_authenticate_with_external_service),
    path("api/post/create/", views.view_create_post),
    path("api/post/get/", views.view_get_posts),
    path("api/post/get/<str:post_id>", views.view_get_post),
    path("api/post/update/<str:post_id>", views.view_update_post),
    path("api/post/delete/<str:post_id>", views.view_delete_post),
    path("api/post/upvote/<str:post_id>", views.view_upvote_post),
    path("api/post/downvote/<str:post_id>", views.view_downvote_post),
    path("api/user/register", views.view_register_user),
    path("api/user/login", views.view_login_user),
    path("api/user/profile/<str:user_id>", views.view_get_user_profile),
    path("api/user/update/<str:user_id>", views.view_delete_user_profile),
]
