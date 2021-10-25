from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm
from django.core.mail import send_mail
# Create your views here.

# view for post list
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
    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
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
    
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent':sent})
