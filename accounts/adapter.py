from allauth.account.adapter import DefaultAccountAdapter


class RecruiterAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        if data.get('is_recruiter'):
            user.is_recruiter = True
        user.save()
        return user
