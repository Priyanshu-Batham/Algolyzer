from django import forms

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

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        label="Email Address",
        required=True,
    )

    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "+1234567890"}
        ),
        label="Phone Number",
        max_length=15,
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

    course = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Course Enrolled",
        max_length=100,
        required=True,
    )

    enrollment_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        label="Enrollment Date",
    )

    class Meta:
        model = UserProfile
        fields = [
            "full_name",
            "dob",
            "email",
            "phone_number",
            "gender",
            "address",
            "course",
            "enrollment_date",
        ]
