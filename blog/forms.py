from django import forms
from .models import Comment

class ShareForm(forms.Form):
    name    = forms.CharField(max_length=255)
    email   = forms.EmailField()
    to      = forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea({'rows':'5'}))

class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea({'rows':'3'}))
    class Meta:
        model = Comment
        fields = ('text',)
