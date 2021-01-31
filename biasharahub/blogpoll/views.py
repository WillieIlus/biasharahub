from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.encoding import uri_to_iri
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from accounts.decorators import UserRequiredMixin
from biasharahub import settings
from comments.forms import CommentForm
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from .forms import PostPollForm, PollChoiceFormSet, PostChoiceForm
from .models import PostPoll, PostChoice


class PostPollCreate(LoginRequiredMixin, CreateView):
    model = PostPoll
    form_class = PostPollForm
    template_name = 'posts/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['choice_form'] = PollChoiceFormSet(self.request.POST, instance=self.object)
        else:
            context['choice_form'] = PollChoiceFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        context = self.get_context_data(form=form)
        formset = context['choice_form']

        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.user = self.request.user
            formset.save()
            return response
        else:
            return super().form_invalid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'There was an error in this form')
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        messages.success(self.request, 'Your postpoll was successful')
        return reverse('post:detail', kwargs={'slug': self.object.slug})


class PostPollEdit(LoginRequiredMixin, UserRequiredMixin, UpdateView):
    model = PostPoll
    form_class = PostPollForm
    template_name = 'posts/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['choice_form'] = PollChoiceFormSet(self.request.POST, instance=self.object)
        else:
            context['choice_form'] = PollChoiceFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        context = self.get_context_data(form=form)
        formset = context['choice_form']

        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.user = self.request.user
            formset.save()
            return response
        else:
            return super().form_invalid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'There was an error in this form')
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        messages.success(self.request, 'Your postpoll was successful')
        return reverse('post:detail', kwargs={'slug': self.object.slug})


class PostPollList(ListView):
    model = PostPoll
    context_object_name = 'post'
    template_name = 'posts/list.html'
    paginate_by = 10


class PostPollDetail(SingleObjectMixin, HitCountMixin, ListView):
    model = PostPoll
    paginate_by = 10
    context_object_name = 'post'
    template_name = 'posts/detail.html'
    count_hit = True

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=PostPoll.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.choices.all()

    def get_object(self, **kwargs):
        slug = self.kwargs.get('slug')
        return get_object_or_404(PostPoll, slug=uri_to_iri(slug))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostChoiceForm()
        context['comment_form'] = CommentForm()
        context['related_business'] = self.object.services.similar_objects()
        context['timezone'] = settings.TIME_ZONE

        if self.object:
            hit_count = get_hitcount_model().objects.get_for_object(self.object)
            hits = hit_count.hits
            context['hitcount'] = {'pk': hit_count.pk}

            if self.count_hit:
                hit_count_response = self.hit_count(self.request, hit_count)
                if hit_count_response.hit_counted:
                    hits = hits + 1
                context['hitcount']['hit_counted'] = hit_count_response.hit_counted
                context['hitcount']['hit_message'] = hit_count_response.hit_message

            context['hitcount']['total_hits'] = hits

        return context


class PostChoicesView(LoginRequiredMixin, UserRequiredMixin, CreateView):
    model = PostChoice
    form_class = PostChoiceForm
    template_name = 'includes/form.html'

    # success_message = "updated successfully"

    def get_success_url(self):
        messages.success(self.request, 'Your choice was successful, and will be approved by an admin')
        return reverse('post:detail', kwargs={'slug': self.object.poll.slug})

    def form_valid(self, form):
        form.instance.poll = get_object_or_404(PostPoll, slug=self.kwargs['slug'])
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'There was an error in this form')
        return self.render_to_response(self.get_context_data(form=form))


class UserPostPolls(ListView):
    context_object_name = 'review'
    template_name = 'posts/user_posts.html'

    def get_queryset(self):
        user = self.request.user
        return PostPoll.objects.filter(user=user).order_by('-publish')
