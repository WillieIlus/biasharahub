from builtins import super

from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Row, Submit, Div
from django import forms
from django.forms import ModelForm, Textarea, RadioSelect, inlineformset_factory

from .models import Review, ReviewImage


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content']
        widgets = {
            'rating': RadioSelect(),
            'content': Textarea(attrs={'cols': 40, 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Div(
                    Div(
                        InlineRadios('rating', css_class='give_rating'),
                        css_class='br-wrapper br-theme-fontawesome-stars m-left-15'
                    ),
                    css_class='atbd_rating_stars',
                ),
            ),
            Row(
                Column('content', css_class='mt-10 form-group col-md-12 mb-0'),
                css_class='form-row', css_id='review_content'
            ),
            Submit('submit', 'Submit', css_class='btn btn-gradient btn-gradient-two')
        )


ReviewPhotoFormSet = inlineformset_factory(Review, ReviewImage, fields=('img', 'alt'),
                                             widgets={'img': forms.FileInput(attrs={
                                                 'class': 'form-control',
                                                 'placeholder': 'Upload photo Image'
                                             }),
                                                 'alt': forms.TextInput(attrs={
                                                     'class': 'form-control',
                                                     'placeholder': 'Describe image'
                                                 })},
                                             labels={'img': '',
                                                     'alt': ''},
                                             form=ReviewForm, extra=4)


class ReviewPhotoFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ReviewPhotoFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            Row(
                Column('img', css_class='mt-10 form-group col-md-5 mb-0'),
                Column('alt', css_class='mt-10 form-group col-md-7 mb-0'),
                css_class='form-row'
            ),
        )
        self.add_input(Submit("submit", "Save", css_class='btn btn-gradient'))
