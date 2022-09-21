from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    # post views
    # list of posts
    path("", views.post_list, name="post_list"),
    # post details
    path("<int:id>/", views.post_detail, name="post_detail"),
]
