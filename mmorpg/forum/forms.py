from django import forms
from .models import Post
from froala_editor.widgets import FroalaEditor


class PostForm(forms.ModelForm):
    heading = forms.CharField(label="Заголовок")
    text = forms.CharField(label="Текст", widget=FroalaEditor)
    types = forms.ChoiceField(choices=Post.get_types(), label="Категория")

    class Meta:
        model = Post
        fields = [
            'heading',
            'text',
            'types',
        ]