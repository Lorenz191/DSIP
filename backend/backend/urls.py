from django.contrib import admin
from django.urls import path
from .DSIP import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sean/<str:text>/", views.sean_view),
    path(
        "api/admin/",
    ),
    path("api/posts/"),
]
