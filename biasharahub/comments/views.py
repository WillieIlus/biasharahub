from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from accounts.decorators import UserRequiredMixin
from comments.forms import CommentForm
from reviews.models import Review
from .models import Comment


class CommentCreateMixin:
    model = Comment
    form_class = CommentForm
    template_name = 'includes/form.html'

    def form_valid(self, form):
        form.instance.content_object = get_object_or_404(Review, slug=self.kwargs['slug'])
        form.instance.user = self.request.user
        parent_obj = None
        try:
            parent_id = int(self.request.POST.get("parent_id"))
        except:
            parent_id = None
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()
        form.parent = parent_obj
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'There was an error in this form')
        return self.render_to_response(self.get_context_data(form=form))


class CommentReview(LoginRequiredMixin, CommentCreateMixin, CreateView):
    # model = Comment
    # form_class = CommentForm
    # template_name = 'includes/form.html'

    def get_success_url(self):
        return reverse('reviews:detail', kwargs={'slug': self.object.content_object.slug})


class CommentReviewBusiness(LoginRequiredMixin, CommentCreateMixin, CreateView):


    def get_success_url(self):
        # return reverse('reviews:detail', kwargs={'slug': self.object.content_object.slug})
        return reverse('business:detail', kwargs={'slug': self.object.content_object.content_object.slug})


class CommentEdit(LoginRequiredMixin,  UserRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'includes/form.html'


class CommentList(ListView):
    model = Comment
    context_object_name = 'comment'
    template_name = 'comments/list.html'


class CommentDetail(DetailView):
    model = Comment
    context_object_name = 'comment'
    template_name = 'comments/detail.html'


class UserComments(ListView):
    context_object_name = 'comment'
    template_name = 'comments/user_comments.html'

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(user=user).order_by('-publish')
