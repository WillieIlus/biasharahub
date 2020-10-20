from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View

from business.models import Business
from favourites.models import Bookmark, Vote
from reviews.models import Review


@login_required
def bookmark_company(request, slug):
    user = request.user
    model = get_object_or_404(Business, slug=slug)
    bookmark = model.bookmark.filter(user=user).first()
    if user.is_authenticated:
        if bookmark is not None:
            bookmark.delete()
        else:
            bookmark = Bookmark()
            bookmark.user = request.user
            bookmark.content_object = model
            bookmark.save()
        return HttpResponseRedirect(model.get_url_path())
    else:
        messages.warning(request, 'you must be authenticated first')


@login_required
def vote_up(request, slug):
    user = request.user
    model = get_object_or_404(Review, slug=slug)
    vote_up = model.votes.filter(user=user, vote=Vote.LIKE).first()
    vote_down = model.votes.filter(user=user, vote=Vote.DISLIKE).first()
    if vote_up is not None:
        vote_up.delete()
    elif vote_down is not None and vote_up is None:
        vote_down.delete()
        vote_up = Vote()
        vote_up.user = request.user
        vote_up.content_object = model
        vote_up.vote = Vote.LIKE
        vote_up.save()
    else:
        vote_up = Vote()
        vote_up.user = request.user
        vote_up.content_object = model
        vote_up.vote = Vote.LIKE
        vote_up.save()
    return HttpResponseRedirect(model.get_url_path())


@login_required
def vote_down(request, slug):
    user = request.user
    model = get_object_or_404(Review, slug=slug)
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
    return HttpResponseRedirect(model.get_url_path())


class ReviewVoteUp(View):

    def post(self, request, slug):
        model = get_object_or_404(Review, slug=slug)
        like = Vote.LIKE
        user = request.user

        try:
            vote_up = Vote.objects.get(content_type=model, object_id=model.id, user=user)
            if vote_up.vote is not None:
                vote_up.delete()
                result = False

            else:
                vote_up.vote = like
                vote_up.save(update_fields=['vote'])
                result = True
        except Vote.DoesNotExist:
            model.votes.create(user=user, vote=like)
            result = True
        return HttpResponseRedirect(model.get_url_path)

#
# class VotesView(View):
#     model = None
#     vote_type = None
#
#     def post(self, request, slug):
#         obj = self.model.objects.get(slug=slug)
#         try:
#             vote = Vote.objects.get(content_type=ContentType.objects.get_for_model(obj),  object_id=obj.id, user=request.user)
#             if vote.vote is not self.vote_type:
#                 vote.vote = self.vote_type
#                 vote.save(update_fields=['vote'])
#                 result = True
#             else:
#                 vote.delete()
#                 result = False
#         except Vote.DoesNotExist:
#             obj.votes.create(user=request.user, vote=self.vote_type)
#             result = True
#         return HttpResponseRedirect(model.get_url_path)
#
#
