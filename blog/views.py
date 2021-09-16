from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def post_list(request):
    object_list = Post.published.all()

    #pagination
    paginator = Paginator(object_list, per_page=3)      #3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        #If page number is not an integer, deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        #If page number is out of range, deliver the last page of the results
        posts = paginator.page(paginator.num_pages)
    #/pagination
    return render(
        request,
        'blog/post/list.html',
        {'page': page,
         'posts': posts}
    )

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day
        )
    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )