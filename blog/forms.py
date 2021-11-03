from django import forms
from django.db.models import query
from .models import Comment

# Form for post sharing functionality
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

# Form for comments in a post
class CommentForm(forms.ModelForm):
    class Meta:                 # indicate which model to use and django will automatically
        model = Comment         # introspect and builds the form dynamically
        fields = ('name', 'email', 'body')      # only these 3 fields need to appear in the
                                                # form as user can fill on these 3

# Form for full text search functionality
class SearchForm(forms.Form):
    query = forms.CharField()