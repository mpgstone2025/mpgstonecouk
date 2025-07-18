from django import forms
from tinymce.widgets import TinyMCE
from .models import Blog

class BlogForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Blog
        fields = '__all__'
