from django import forms
from django.contrib.auth.forms import UserCreationForm
from wtpixel.models import Image, Video, Music
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    # email = forms.CharField(
    #     widget=forms.EmailInput(
    #         attrs={
    #             "placeholder": "Email",
    #             "class": "form-control"
    #         }
    #     ))

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=50, help_text='Required a valid email address.')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput(),
                                help_text='Enter the same password as before, for Verification')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'file', 'tag')

        def save(self):
            image = super(ImageForm, self).save()
            return image


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('title', 'file', 'tag')

        def save(self):
            video = super(VideoForm, self).save()
            return video


class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ('title', 'file', 'tag')

        def save(self):
            music = super(MusicForm, self).save()
            return music
