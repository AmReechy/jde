from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-input"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-input"}))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone_number", "postal_address", "password"]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Type your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Type your last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Input valid email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Input correct phone number'}),
            'postal_address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Type correct address'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned_data


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-input"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-input"}))

