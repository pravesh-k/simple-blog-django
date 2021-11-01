from django import template
from django.db import reset_queries
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

# to register custom template tags and filters
register = template.Library()

# template tag to return the total number of published posts
@register.simple_tag
def total_posts():
    return Post.published.count()

# template tag to return the latest published posts
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    args = {'latest_posts': latest_posts}
    return args

# template tag to return the posts with max comments
@register.simple_tag
def get_most_commented_posts(count = 5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

# template filter to enable us to use markdown
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))