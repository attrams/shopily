from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Post

from taggit.models import Tag

# Create your views here.


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    recent_three_posts = post_list[:3]
    tags = Tag.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    # pagination with 4 blog post per page
    paginator = Paginator(object_list=post_list, per_page=4)
    page_number = request.GET.get('page', 1)
    posts = paginator.page(number=page_number)

    return render(
        request,
        'blog/post/list.html',
        {
            # this posts is the main list of post which contains pagination
            'posts': posts,
            'tags': tags,
            'section': 'blog',
            'posts_count': len(post_list),
            'recent_three_posts': recent_three_posts,
            'tag': tag
        }
    )


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        klass=Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    return render(request, 'blog/post/detail.html', {'post': post, 'section': 'blog_detail'})
