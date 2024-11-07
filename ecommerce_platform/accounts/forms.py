from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Custom form for user registration extending Django's UserCreationForm.
    Adds additional fields for email, date of birth, and other user information.
    """
    email = forms.EmailField(label=_('Email Address'), required=True)
    date_of_birth = forms.DateField(
        label=_('Date of Birth'),
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        # Add Bootstrap classes to all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        self.fields['password1'].required = True
        self.fields['password2'].required = True

        for field in ['password1', 'password2']:
            self.fields[field].help_text = None

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            'email', 'first_name', 'last_name', 'date_of_birth', 'gender', 'country',
        )
        labels = {
            'username': _('Username'),
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'gender': _('Gender'),
            'country': _('Country'),
            'password1': _('Password'),
            'password2': _('Password Confirmation'),
        }


class CustomAuthenticationForm(AuthenticationForm):
    """
    Custom authentication form that uses email instead of username.
    Customizes error messages and widget attributes for email-based login.
    """
    username = forms.EmailField(
        label=_('Email Address'),
        widget=forms.TextInput(attrs={'autofocus': True})
    )

    error_messages = {
        'invalid_login': _('Please enter a correct email and password.'),
        'inactive': _('This account is inactive.'),
    }
