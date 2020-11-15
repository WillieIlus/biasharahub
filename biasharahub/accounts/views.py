from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import UpdateView, DetailView, ListView
from django.views.generic.detail import SingleObjectMixin

from business.models import Business
from comments.models import Comment
from accounts.decorators import UserRequiredMixin
from .forms import UserForm, SocialProfileFormSet
from .models import User


#
# class SignUp(View):
#     def get(self, request):
#         form = SignUpForm()
#         return render(request, 'registration/signup.html', {'form': form})
#
#     def post(self, request):
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.set_unusable_password()
#             user.save()
#
#             subject = 'Activate your accounts.'
#             current_site = get_current_site(request)
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
#             token = account_activation_token.make_token(user)
#             activation_link = '{0}/?uid={1}&token{2}'.format(current_site, uid, token)
#             message = "Hello {0}, {1}".format(user.email, activation_link)
#             sender = None  # Added later
#             recipients = form.cleaned_data.get('email')
#             # email = EmailMessage(subject, message, [recipients])
#             # email.send()
#             send_mail(subject, message, sender, [recipients])
#         return HttpResponse("please confirm your email address to complete your registration")
#
#
# class Activate(View):
#     def get(self, request, uidb64, token):
#         try:
#             uid = force_text(urlsafe_base64_encode(uidb64))
#             user = User.objects.get(pk=uid)
#         except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None
#             if user is not None and account_activation_token.check_token(user, token):
#                 user.is_active = True
#                 user.save()
#                 login(request, user)
#
#                 form = PasswordChangeForm(request.user)
#                 return render(request, 'registration/activation.html', {'form': form})
#             else:
#                 return HttpResponse('Activation link is invalid!')
#
#     def post(self, request):
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)
#             return HttpResponse("Pass word changed successfully")
#
#
# class SignUpView(CreateView):
#     model = User
#     form_class = SignUpForm
#     template_name = 'registration/signup.html'
#
#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('accounts:dashboard')
#
#
# class UserLogin(LoginView):
#     model = User
#     form_class = LoginForm
#     template_name = 'accounts/login.html'
#
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     context['title'] = "Login"
#     #     return context
#
#     def form_valid(self, form):
#         email = self.request.POST['email']
#         password = self.request.POST['password']
#         user = authenticate(email=email, password=password)
#         if user is not None:
#             # if user.is_active:
#             #     login(self.request, user)
#             return HttpResponseRedirect('accounts:dashboard')
#
#
# class UserLogout(LogoutView):
#     # template_name = 'accounts/logout.html'
#
#     def get_object(self):
#         return self.request.user


class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserForm
    template_name = 'includes/form.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('accounts:dashboard')


class Dashboard(LoginRequiredMixin, DetailView):
    template_name = 'account/dashboard.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['user'] = self.object
        context['form'] = UserForm()
        return context


class Detail(LoginRequiredMixin, SingleObjectMixin, ListView):
    # model = User
    paginate_by = 6
    template_name = 'account/detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=User.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object
        context['business'] = Business.objects.filter(user=self.object)[:4]
        context['comments'] = Comment.objects.filter(user=self.object)
        return context

    def get_queryset(self):
        return self.object.review_set.all()


class SocialProfile(LoginRequiredMixin, UserRequiredMixin, UpdateView):
    model = Business
    # form_class = BusinessNameFormi
    fields = 'first_name'
    template_name = 'business/form.html'
    # success_url = self.model.get_absolute_url
    success_message = "updated successfully"

    def get_success_url(self):
        return reverse('business:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['social_form'] = SocialProfileFormSet(self.request.POST, instance=self.object)
            context['social_form'].full_clean()

        else:
            context['social_form'] = SocialProfileFormSet(instance=self.object)

        return context

    def form_valid(self, form):
        # form.instance.user = self.request.user
        # form.save()

        context = self.get_context_data(form=form)
        formset = context['social_form']

        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)

def hide_mail(request, pk):
    user = get_object_or_404(User, pk=pk)
    hidden = user.hide_mail

    if hidden:
        user.hide_mail = False
        user.save()
    else:
        user.hide_mail = True
        user.save()

    return HttpResponseRedirect(user.get_absolute_url())


def hide_phone(request, pk):
    user = get_object_or_404(User, pk=pk)
    hidden = user.hide_phone
    if hidden:
        user.hide_phone = False
        user.save()
    else:
        user.hide_phone = True
        user.save()

    return HttpResponseRedirect(user.get_absolute_url())
