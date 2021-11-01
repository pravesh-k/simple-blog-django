from django import template
from django.db import reset_queries
from ..models import Post

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    # print('\n\n\n', latest_posts, '\n\n\n')
    args = {'latest_posts': latest_posts}
    return args