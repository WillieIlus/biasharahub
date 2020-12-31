from import_export import resources

from accounts.models import User


class UserResource(resources.ModelResource):
    class Meta:
        model = User
