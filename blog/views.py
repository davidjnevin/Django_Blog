from django.shortcuts import get_object_or_404, render

from .models import Post


def post_detail(request, id):
    """Return a specific post by 'id'."""
    post = get_object_or_404(Post, id=id, status=Post.Status.Published)

    return render(request, "blog/post/detail.html", {"post": post})


def post_list(request):
    """Generate a list of all published posts."""
    posts = Post.published.all()
    return render(request, "blog/post/list.html", {"posts": posts})
