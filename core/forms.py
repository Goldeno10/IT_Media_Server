from django.contrib.auth.forms import UserCreationForm
from core.models import User


class SignUpForm(UserCreationForm):
    """ Signup form """
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        help_texts = {
            'username': None,
        }
