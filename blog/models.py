from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse


class PublishedManager(models.Manager):
    """Custom model manager for published posts."""

    def get_queryset(self):
        """Return only published posts."""
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    """Post model: title, slug, body, publish, created, updated, and status."""

    class Status(models.TextChoices):
        """Post.Status.choices = [('DF', 'DRAFT'), ('PB', 'PUBLISHED')] ."""

        DRAFT = "DF", "DRAFT"
        PUBLISHED = "PB", "PUBLISHED"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )

    objects = models.Manager()  # The default Manager
    published = PublishedManager()  # Custom manager for Published posts

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def __str__(self):
        """Return title."""
        return self.title

    def get_absolute_url(self):
        return reverse(
            "blog:post_detail",
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug,
            ],
        )
