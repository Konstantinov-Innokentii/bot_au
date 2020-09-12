from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django import forms


from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )

    class Meta:
        model = CustomUser
        fields = [*UserCreationForm.Meta.fields, 'email']
