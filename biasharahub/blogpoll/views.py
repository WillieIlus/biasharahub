from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.encoding import uri_to_iri
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from accounts.decorators import UserRequiredMixin
from biasharahub import settings
from comments.forms import CommentForm
from favourites.models import Vote
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
    queryset = PostPoll.published.all()
    context_object_name = 'post'
    template_name = 'posts/list.html'
    paginate_by = 9


class PostPollDetail(SingleObjectMixin, HitCountMixin, ListView):
    # model = PostPoll
    paginate_by = 10
    context_object_name = 'post'
    template_name = 'posts/detail.html'
    count_hit = True

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=PostPoll.published.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.choices.annotate(num_likes=Count('votes')).order_by('-num_likes', '-rank')

    def get_object(self, **kwargs):
        slug = self.kwargs.get('slug')
        return get_object_or_404(PostPoll, slug=uri_to_iri(slug))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostChoiceForm()
        context['comment_form'] = CommentForm()
        context['related_posts'] = self.object.tags.similar_objects()[:3]
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


class PostChoicesView(LoginRequiredMixin, CreateView):
    model = PostChoice
    form_class = PostChoiceForm
    template_name = 'includes/form.html'

    # success_message = "updated successfully"

    def get_success_url(self):
        messages.success(self.request, 'Your choice was successful')
        return reverse('post:detail', kwargs={'slug': self.object.poll.slug})

    def form_valid(self, form):
        form.instance.poll = get_object_or_404(PostPoll, slug=self.kwargs['slug'])
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'There was an error in this form')
        return self.render_to_response(self.get_context_data(form=form))


class UserPostPolls(ListView):
    context_object_name = 'post'
    template_name = 'posts/user_posts.html'

    def get_queryset(self):
        user = self.request.user
        return PostPoll.objects.filter(user=user).order_by('-publish')



@login_required
def vote_up(request, slug):
    user = request.user
    model = get_object_or_404(PostChoice, slug=slug)
    vote_up = model.votes.filter(user=user, vote=Vote.LIKE).first()
    vote_down = model.votes.filter(user=user, vote=Vote.DISLIKE).first()
    if model.poll.active:
        if vote_up is not None:
            vote_up.delete()
        elif vote_down is not None and vote_up is None:
            vote_down.delete()
            vote_up = Vote()
            vote_up.user = request.user
            vote_up.content_object = model
            vote_up.vote = Vote.LIKE
            vote_up.save()
            messages.success(request, 'OK! you successfully removed your vote.')
        else:
            vote_up = Vote()
            vote_up.user = request.user
            vote_up.content_object = model
            vote_up.vote = Vote.LIKE
            vote_up.save()
            messages.success(request, 'Hurrah! your vote was successful')
        return HttpResponseRedirect(model.poll.get_url_path())
    else:
        messages.warning(request, "Oops! You can't vote now. Voting for this post has been closed")
        return HttpResponseRedirect(model.poll.get_url_path())


@login_required
def vote_down(request, slug):
    user = request.user
    model = get_object_or_404(PostChoice, slug=slug)
    vote_up = model.votes.filter(user=user, vote=Vote.LIKE).first()
    vote_down = model.votes.filter(user=user, vote=Vote.DISLIKE).first()
    if vote_down is not None:
        vote_down.delete()
    elif vote_up is not None and vote_down is None:
        vote_up.delete()
        vote_down = Vote()
        vote_down.user = request.user
        vote_down.content_object = model
        vote_down.vote = Vote.DISLIKE
        vote_down.save()
    else:
        vote_down = Vote()
        vote_down.user = request.user
        vote_down.content_object = model
        vote_down.vote = Vote.DISLIKE
        vote_down.save()
    return HttpResponseRedirect(model.poll.get_url_path())




@login_required
def endpoll(request, slug):
    poll = get_object_or_404(PostPoll, slug=slug)
    if request.user != poll.user:
        return redirect('home')

    if poll.active is True:
        poll.active = False
        poll.save()
        return HttpResponseRedirect(poll.get_url_path())
    else:
        return HttpResponseRedirect(poll.get_url_path())
