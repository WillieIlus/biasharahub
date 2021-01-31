from builtins import super

from crispy_forms.bootstrap import InlineRadios, InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms
# from django.contrib.admin import widgets
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from haystack.forms import FacetedSearchForm
from pagedown.widgets import PagedownWidget

from business.models import Business, BusinessImage, CompanySocialProfile
from categories.models import Category
from locations.models import Location
from reviews.models import RATING_CHOICES


class BusinessNameForm(ModelForm):
    name = forms.CharField(disabled=True)

    class Meta:
        model = Business
        fields = ('name',)


class BusinessAddForm(ModelForm):
    logo = forms.ImageField(label='', required=False, widget=forms.FileInput(attrs={'placeholder': 'your logo'}))
    description = forms.CharField(widget=PagedownWidget(attrs={'placeholder': 'Describe your biashara'}))
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Your biashara name'}))
    email = forms.EmailField(label='', required=False, widget=forms.TextInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = Business
        fields = (
            'name', 'logo', 'email', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'name',
            'logo',
            'email',
            'description'
        )


class BusinessForm(ModelForm):
    logo = forms.ImageField(label='logo', required=False,
                            widget=forms.ClearableFileInput(attrs={'placeholder': 'Logo',
                                                                   'class': 'btn btn-outline-secondary'}))
    description = forms.CharField(widget=PagedownWidget(attrs={'placeholder': 'Describe your biashara'}))
    location = forms.ModelChoiceField(widget=forms.RadioSelect(), required=False, queryset=Location.objects.all(), )

    category = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                              required=False, queryset=Category.objects.all(), )

    class Meta:
        model = Business
        fields = (
            'name', 'logo', 'email', 'hide_mail', 'phone', 'hide_phone', 'description', 'website', 'location',
            'category', 'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'name',
            'logo',
            'email',
            'hide_mail',
            'phone',
            'hide_phone',
            'description',
            'website',
            InlineCheckboxes('category'),
            InlineRadios('location'),
            'address',
            'services',
        )


class AddCategoryForm(ModelForm):
    location = forms.ModelChoiceField(widget=forms.RadioSelect(), required=False, queryset=Location.objects.all(), )

    category = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), required=False,
                                              queryset=Category.objects.all(), )

    class Meta:
        model = Business
        fields = ('address', 'location', 'category', 'services')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            InlineCheckboxes('category'),
            InlineRadios('location'),
            'address',
            'services',
        )


class BusinessFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        label=_("Category"), required=False, queryset=Category.objects.all(),
    )
    location = forms.ModelChoiceField(label=_("Location"), required=False, queryset=Location.objects.all(), )
    rating = forms.ChoiceField(label=_("Rating"), required=False, choices=RATING_CHOICES, )


class BusinessPhotoForm(ModelForm):
    img = forms.ImageField(label='Image', )
    alt = forms.CharField(label='Describe the Image', )

    class Meta:
        model = BusinessImage
        fields = ('business', 'img', 'alt')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'business',
            Row(
                Column('img', css_class='mt-10 form-group col-md-6 mb-0'),
                Column('alt', css_class='mt-10 form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
        )


class BusinessPhotoFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(BusinessPhotoFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            Row(
                Column('img', css_class='mt-10 form-group col-md-4 mb-0'),
                Column('alt', css_class='mt-10 form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
        )
        self.add_input(Submit("submit", "Save", css_class='btn btn-gradient btn-gradient-one'))


class SocialProfileForm(ModelForm):
    class Meta:
        model = CompanySocialProfile
        fields = ('business', 'network', 'username', 'url')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('business', css_class='mt-10 form-group col-md-3 mb-0'),
                Column('network', css_class='mt-10 form-group col-md-3 mb-0'),
                Column('username', css_class='mt-10 form-group col-md-3 mb-0'),
                Column('url', css_class='mt-10 form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
        )


SocialProfileFormSet = inlineformset_factory(Business, CompanySocialProfile,
                                             fields=['business', 'network', 'username', 'url'],
                                             can_delete=True, exclude=None, extra=3, max_num=9)


class BusinessSearchForm(FacetedSearchForm):

    def __init__(self, *args, **kwargs):
        data = dict(kwargs.get("data", []))
        self.category = data.get('category', [])
        self.location = data.get('location', [])
        # self.location = data.get('address', [])
        # self.location = data.get('services', [])
        super(BusinessSearchForm, self).__init__(*args, **kwargs)

    def search(self):
        sqs = super(BusinessSearchForm, self).search()
        if self.category:
            query = None
            for category in self.category:
                if query:
                    query += u' OR '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(category)
            sqs = sqs.narrow(u'category_exact:%s' % query)
        if self.location:
            query = None
            for location in self.location:
                if query:
                    query += u' OR '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(location)
            sqs = sqs.narrow(u'location_exact:%s' % query)
        # if self.address:
        #     query = None
        #     for address in self.address:
        #         if query:
        #             query += u' OR '
        #         else:
        #             query = u''
        #         query += u'"%s"' % sqs.query.clean(address)
        #     sqs = sqs.narrow(u'location_exact:%s' % query)
        # if self.services:
        #     query = None
        #     for services in self.services:
        #         if query:
        #             query += u' OR '
        #         else:
        #             query = u''
        #         query += u'"%s"' % sqs.query.clean(services)
        #     sqs = sqs.narrow(u'location_exact:%s' % query)
        return sqs
