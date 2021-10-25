from django.db import models
from django.db.models.expressions import OrderBy
from django.db.models.manager import Manager
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

# Create your models here.

class Post(models.Model):
    objects = models.Manager()              #default manager
    published = PublishedManager()          #custom manager
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        unique_for_date='publish'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    
    def get_absolute_url(self):
        # print("\n\n\n"+str(self.slug)+"\n\n\n")
        return reverse(
            'blog:post_detail',
            args=[self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug]
        )
    
    class Meta:
        ordering = ('-publish',)
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(       # to which post the comment object is associated with
        Post,
        on_delete=models.CASCADE,
        related_name='comments'     # this attribute is used to backtrack to the this object from post object
        )
    
    name = models.CharField(max_length=80)      # name of user who commented
    email = models.EmailField()                 # name of email who commented
    body = models.TextField()                   # body of the comment
    created = models.DateTimeField(auto_now_add=True)       # timestamp of comment creation
    updated = models.DateTimeField(auto_now=True)           # timestamp of comment updation
    active = models.BooleanField(default=True)              # flag for inappropriate comment

    class Meta:
        ordering = ('created',)                 # sort comments by creation timestamp
    
    def __str__(self) -> str:
        return f'Comment by {self.name} on {self.post}'