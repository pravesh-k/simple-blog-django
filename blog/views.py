from django.contrib.postgres import search
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
# Create your views here.

# view for post list
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug = tag_slug)
        object_list = object_list.filter(tags__in=[tag])

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

    args = {
            'page': page,
            'posts': posts,
            'tag': tag
            }
    return render(
        request,
        'blog/post/list.html',
        args
        )

# view for post details
def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day
        )

        # List of active comments for this post
    comments = post.comments.filter(active=True)
    
    new_comment = None

    if request.method == 'POST':
        # A comment is posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Capture comment from the form but don't save to DB yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the DB
            new_comment.save()

    else:
        comment_form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    args = {                                # data to be passed to the template for rendering
            'post': post,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form,
            'similar_posts': similar_posts
            }
            
    return render(
        request,
        'blog/post/detail.html',
        args
        )

# view for the form which handles sending post in mails
def post_share(request, post_id):

    print('REQUEST: ', request)
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status = 'published')
    sent = False

    if request.method == 'POST':
        # when form was submitted, create a form instance using the
        # submitted data that is contained in request.POST 
        form = EmailPostForm(request.POST)
        # print("FORM Data: ", form)
        if form.is_valid():
            # Form fields passed validation, If your form data does not 
            # validate, cleaned_data will contain only the valid fields.
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'praveshnayak@gmail.com', [cd['to']])
            sent = True
            # ...send email

        # When the view is loaded initially with a GET request, you create a new form
        # instance that will be used to display the empty form in the template
    else:
        form = EmailPostForm()
    
    args = {
        'post': post, 
        'form': form, 
        'sent':sent
        }
    return render(request, 'blog/post/share.html', args)


# view for full-text search 
def post_search(request):
    form = SearchForm()     #instantiate a SearchForm object
    query = None
    results = []

    if 'query' in request.GET:              #initialize the form oject with dict data of 
        form = SearchForm(request.GET)      #request.GET if query is present in request.GET object
        if form.is_valid():
            query = form.cleaned_data['query']      #fetch the value of query of form object is valid
                                                    #fetching posts matching the search query
            # search_vector = SearchVector('title', weight='A') + \
                            # SearchVector('body', weight='B')        #giving weights to title and body
            # search_query = SearchQuery(query)
            results = Post.published.annotate(      
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.1).order_by('-similarity')
    
    args = {
        'form': form,
        'query': query,
        'results': results
        }

    #returning an httpResponse object to the search.html template with the context data/args
    return render(
        request,
        'blog/post/search.html',
        args
        )