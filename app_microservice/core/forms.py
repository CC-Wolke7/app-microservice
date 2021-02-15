from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class EmailAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.fields['username'].label = 'Email'
        self.request = request

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, email=username, password=password
            )

            if self.user_cache is None:
                raise self.get_invalid_login_error()

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': 'email'},
        )


class AdminLoginForm(EmailAuthenticationForm):
    """
    A custom authentication form used in the admin app.
    """
    error_messages = {
        **AuthenticationForm.error_messages,
        'invalid_login': _(
            'Please enter the correct email and password for a staff '
            'account. Note that both fields may be case-sensitive.'
        ),
    }

    required_css_class = 'required'

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)

        if not user.is_staff:
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': 'email'}
            )
