from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm

from creovate.account.models import Profile, Wallet


class RegisterForm(UserCreationForm):

    class Meta:
        model = Profile
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'required': True,
            'placeholder': 'Enter a valid email address.',
        })

        self.fields['username'].widget.attrs.update({
            'required': True,
            'placeholder': 'Enter username.',
            'class': 'form-control',
        })

        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Your first name',
        })

        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Your last name',
        })

        self.fields['password1'].help_text = "Password must contain at least 8 characters."
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'required': True,
            'placeholder': 'Enter Password.',
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'required': True,
            'placeholder': 'Enter your password again.',
        })


    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if  len(password1) < 8:
            self.add_error('password1', 'Password must be at least 8 characters.')

        if  len(password2) < 8:
            self.add_error('password2', 'Password must be at least 8 characters.')

        if password1 == username:
            self.add_error('password1', 'Password should not be the same as username.')

        if password2 == username:
            self.add_error('password2', 'Password should not be the same as username.')

        return cleaned_data



class LoginForm(AuthenticationForm):

    class Meta:
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your email account.',
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your password.',
        })


class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        label="",
        widget= forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Your Email',

    }))


class PasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label = "",
        widget= forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Your New Password',
        }),
    )

    new_password2 = forms.CharField(
        label = "",
        widget= forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Your New Password Again',
        }),
    )


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'image_profile']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['image_profile'].widget.attrs.update({
            'class': 'form-control'
        })


class UpdateWalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['balance']

    BALANCE_CHOICES = [
        (2000000, '2000000'),
        (5000000, '5000000'),
        (10000000, '10000000'),
        (20000000, '20000000'),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['balance'] = forms.ChoiceField(
            choices=self.BALANCE_CHOICES,
            widget=forms.Select(attrs={'class': 'form-control'})
        )