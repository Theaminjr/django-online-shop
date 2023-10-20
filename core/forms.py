from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from core.models import User


class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("phone_number",)


class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("phone_number",)