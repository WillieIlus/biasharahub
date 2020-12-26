from django.shortcuts import redirect


class UserRequiredMixin(object):
    """ Making sure that only own user can update """

    def dispatch(self, request, *args, **kwargs):
        response = redirect('account_login')
        obj = self.get_object()
        if not self.request.user.is_superuser:
            if obj.user != self.request.user:
                return response
        else:
            return super(UserRequiredMixin, self).dispatch(request, *args, **kwargs)
        return super(UserRequiredMixin, self).dispatch(request, *args, **kwargs)
