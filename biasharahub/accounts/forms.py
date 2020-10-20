from allauth.account.forms import LoginForm, SignupForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django import forms

from accounts.models import User


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(label='', max_length=254, required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name '}))
    last_name = forms.CharField(label='', max_length=254, required=False,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(label='', max_length=254, required=True,
                             widget=forms.EmailInput(attrs={'placeholder': 'Email is required'}))
    password1 = forms.CharField(label='', max_length=254, required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label='', max_length=254, required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password'}))

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CustomSignupForm, self).save(request)
        # Add your own processing here.
        # You must return the original result.
        return user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'email',
            Row(
                Column('first_name', css_class='mt-10 form-group col-md-6 col-sm-12 mb-0'),
                Column('last_name', css_class='mt-10 form-group col-md-6 col-sm-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='mt-10 form-group col-md-6 col-sm-12 mb-0'),
                Column('password2', css_class='mt-10 form-group col-md-6 col-sm-12 mb-0'),
                css_class='form-row'
            ),
            # 'remember_me',
            Submit('submit', 'Signup', css_class='btn btn-block btn-lg btn-gradient btn-gradient-two'),
        )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'is_freelancer', 'is_entrepreneur', 'photo', 'bio', 'website', 'address',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('is_freelancer', css_class='mt-10 form-group col-md-6 col-sm-12 mb-0'),
                Column('is_entrepreneur', css_class='mt-10 form-group col-md-6 col-sm-12 mb-0'),
                css_class='form-row'
            ),
            'photo',
            Row(
                Column('first_name', css_class='mt-10 form-group col-md-6 col-sm-12 mb-0'),
                Column('last_name', css_class='mt-10 form-group col-md-6 col-sm-12 mb-0'),
                css_class='form-row'
            ),
            'bio',
            'website', 'facebook',
            'twitter', 'linkedin', 'instagram', 'youtube',
            Row(
                Column('address', css_class='mt-10 form-group col-md-6 col-sm-12 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Update Bio', css_class='btn btn-lg btn-gradient btn-gradient-two'),
        )


class CustomLoginForm(LoginForm):

    def login(self, *args, **kwargs):
        # Add your own processing here.
        # You must return the original result.
        return super(CustomLoginForm, self).login(*args, **kwargs)

    class Meta:
        model = User
        fields = (
            # 'username',
            'email',
            'login',
            'login_widget',
            'password',
            'remember',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            # 'username',
            'email',
            'login',
            'login_widget',
            'password',
            'remember',
            Submit('submit', 'Login', css_class='btn btn-block btn-lg btn-gradient btn-gradient-two'),
            # <i class="fa fa-sign-in"></i>

        )
