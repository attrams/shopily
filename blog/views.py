from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Post

# Create your views here.


def post_list(request):
    posts = Post.published.all()
    recent_three_posts = posts[:3]

    # pagination with 4 blog post per page
    paginator = Paginator(object_list=posts, per_page=4)
    page_number = request.GET.get('page', 1)
    post_list = paginator.page(number=page_number)

    return render(
        request,
        'blog/post/list.html',
        {
            'posts': post_list,
            'section': 'blog',
            'posts_count': len(posts),
            'recent_three_posts': recent_three_posts
        }
    )


def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)

    return render(request, 'blog/post/detail.html', {'post': post, 'section': 'blog'})
