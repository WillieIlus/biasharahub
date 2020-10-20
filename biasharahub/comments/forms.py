from builtins import super

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Row, Submit
from django import forms
from django.forms import Textarea

from .models import Comment


class CommentForm(forms.ModelForm):
    content = forms.CharField(label='', required=True, widget=Textarea(attrs={'placeholder': 'Message'}))

    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('content', css_class='mt-10 form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Submit', css_class='btn btn-sm btn-secondary')
        )
