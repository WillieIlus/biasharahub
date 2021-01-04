from allauth.account.models import EmailAddress
from import_export import resources

from accounts.models import User


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class EmailResource(resources.ModelResource):
    class Meta:
        model = EmailAddress
