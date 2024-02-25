from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse

from taggit.managers import TaggableManager
# Create your models here.


class PublishedManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()
    image = models.ImageField(upload_to='blog/%Y/%m/%d', blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse(
            viewname="blog:post_detail",
            kwargs={
                'year': self.publish.year,
                'month': self.publish.month,
                'day': self.publish.day,
                'post': self.slug
            }
        )
