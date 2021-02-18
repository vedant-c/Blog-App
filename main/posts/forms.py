from django import forms
from tinymce.widgets import TinyMCE
from .models import Post,Comment

class TinyMCEWidget(TinyMCE):
    def use_required_attribute(slef,*args):
        return False

class PostForm(forms.ModelForm):
    content=forms.CharField(widget=TinyMCEWidget(attrs={'required':False,'cols':30,'rows':10}))

    class Meta:
        model=Post
        fields=('title','overview','content','categories')

class CommentForm(forms.ModelForm):
    content=forms.CharField(widget=forms.Textarea(attrs=
    {
        'class':'form-control',
        'placeholder':'Type your comment',
        'id':'usercomment',
        'rows':'4'
    }))
    class Meta:
        model=Comment
        fields=('content',)
    