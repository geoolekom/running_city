from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "groups",
        )
        help_texts = {"groups": "В составе этой группы вы будете участвовать в игре"}

    def clean_groups(self):
        value = self.cleaned_data.get("groups")
        if len(value) > 1:
            self.add_error("groups", "Можно находиться не более чем в одной группе одновременно.")
