from builtins import super

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Submit
from django import forms
from django.forms import ModelForm, BaseFormSet
from django.forms.models import inlineformset_factory
from urllib3.connectionpool import xrange

from categories.models import Category
from .models import PostPoll, PostChoice


class PostPollNameForm(ModelForm):
    name = forms.CharField(disabled=True)

    class Meta:
        model = PostPoll
        fields = ('name',)


class PostPollForm(ModelForm):
    image = forms.ImageField(required=False, widget=forms.FileInput())

    # category = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), required=False,
    #                                           queryset=Category.objects.all(), )

    class Meta:
        model = PostPoll
        fields = ("name", "description", "image", "active", "category", "tags", "conclusion")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'name',
            'image',
            'description',
            'active',
            'category',
            'tags',
            'conclusion'
        )


class PostChoiceForm(ModelForm):
    class Meta:
        model = PostChoice
        fields = ("name", "description", 'image', 'url', 'rank')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
                "name",
                "description",
                'image',
                'url',
            'rank',
            Submit('submit', 'Submit', css_class='btn btn-sm btn-secondary')

        )


class PostChoiceFormBaseFormset(BaseFormSet):
    """
    adds request.user to a formset, overwrites BaseFormSet
    """

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def _construct_form(self):  # , i, **kwargs):
        self.forms = []
        for i in xrange(self.total_form_count()):
            self.forms.append(self._construct_form(i, user=self.user))


PollChoiceFormSet = inlineformset_factory(PostPoll, PostChoice,  # formset=PostChoiceFormBaseFormset,
                                          fields=["name", "description", "image", 'url', 'rank'], can_delete=True, extra=8,
                                          max_num=60)
