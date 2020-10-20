from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q

from accounts.models import User

UserModel = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, first_name=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(
                Q(first_name__iexact=first_name) | Q(email__iexact=first_name))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        except MultipleObjectsReturned:
            return User.objects.filter(email=first_name).order_by('id')
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None
