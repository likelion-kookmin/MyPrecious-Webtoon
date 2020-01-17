from django import forms
from .models import *


class CommentForm(forms.ModelForm):
    # text = forms.TextInput(label="댓글")
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget = forms.TextInput(attrs={
            'type':'textarea', 'class': 'textarea is-info', 'style':'height:50px;'
        })
        self.fields['text'].label = ""
