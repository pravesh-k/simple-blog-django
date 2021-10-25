from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:                 # indicate which model to use and django will automatically
        model = Comment         # introspect and builds the from dynamically
        fields = ('name', 'email', 'body')      # only this 3 fields need to appear in the
                                                # form as user can fill on these 3