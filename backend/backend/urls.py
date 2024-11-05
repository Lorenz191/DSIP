from django.contrib import admin
from django.urls import path
from .DSIP import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sean/<str:text>/", views.sean_view),
    path("api/admin/delete/<str:post_id>/", views.view_delete_user_post),
    path("api/admin/comment/<str:post_id>/", views.view_comment_as_admin),
    path("api/external", views.view_authenticate_with_external_service),
    path("api/forum/getPosts", views.view_get_forum_posts),
    path("api/forum/createComment/<str:post_id>", views.view_create_forum_comment),
    path("api/forum/getComments/<str:post_id>", views.view_get_forum_comments),
    path("api/forum/create", views.view_create_forum_post),

]
