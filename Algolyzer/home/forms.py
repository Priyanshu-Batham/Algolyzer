from django import forms

from .models import UserProfile


class UserProfileDOBForm(forms.ModelForm):
    dob = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-control"}
        ),  # HTML5 date picker
        label="Date of Birth",
        required=True,
    )

    class Meta:
        model = UserProfile
        fields = ["dob"]
