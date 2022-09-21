from django.shortcuts import get_object_or_404, render

from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == "POST":
        # form submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # All form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(
                subject, message, "your_account_to_send_email@gmail.com", [cd["to"]]
            )
            sent = True
    else:
        form = EmailPostForm()

    return render(
        request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
    )


def post_list(request):
    """Generate a list of all published posts."""
    post_list = Post.published.all()
    # Pagination using built in paginator
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    # posts = paginator.page(page_number)

    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request, year, month, day, post):
    """Return a specific post by 'id'."""
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    return render(request, "blog/post/detail.html", {"post": post})


class PostListView(ListView):
    """Alternate post list views."""

    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"
