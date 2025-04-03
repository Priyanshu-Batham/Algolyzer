import re
from datetime import date

from django import forms
from django.core.exceptions import ValidationError

from .models import UserProfile


class OnboardingForm(forms.ModelForm):
    dob = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        label="Date of Birth",
        required=True,
    )

    full_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Full Name",
        max_length=100,
        required=True,
    )

    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "+1234567890"}
        ),
        label="Phone Number",
        max_length=15,  # Increased to accommodate country codes
        required=True,
    )

    gender = forms.ChoiceField(
        choices=[("M", "Male"), ("F", "Female"), ("O", "Other")],
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Gender",
        required=True,
    )

    address = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        label="Address",
        required=True,
    )

    class Meta:
        model = UserProfile
        fields = [
            "full_name",
            "dob",
            "phone_number",
            "gender",
            "address",
        ]

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")

        # Remove all non-digit characters
        # cleaned_number = re.sub(r'[^\d+]', '', phone_number)

        # Check if the number contains only digits and optional + at start
        if not re.match(r"^\+?\d+$", phone_number):
            raise ValidationError(
                "Phone number must contain only numbers and an optional + at the start."
            )

        # Check minimum length (adjust according to your requirements)
        if len(phone_number) < 10:
            raise ValidationError("Phone number must be at least 10 digits long.")

        return phone_number

    def clean_dob(self):
        dob = self.cleaned_data.get("dob")
        today = date.today()

        # Calculate age
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        if age < 12:
            raise ValidationError("You must be at least 12 years old to register.")

        return dob
