from django.contrib import admin
from django.urls import path
from .DSIP import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sean/<str:text>/", views.sean_view),
    path("api/admin/<str:post_id>/", views.view_delete_user_post),
    path("api/admin/comment/<str:post_id>/", views.view_comment_as_admin),
]
