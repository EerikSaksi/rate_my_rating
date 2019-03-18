from django import forms
from django.contrib.auth.models import User
from webapp.models import UserProfile, RatingWebsite, Rating, Comment

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'email', 'first_name', 'last_name',)


    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Password does not match")

        return cleaned_data


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',)


class UserProfileForm(forms.ModelForm):
    website = forms.URLField(label='Personal website', required=False)
    picture = forms.ImageField(label="Profile picture", required=False)

    class Meta:
        model = UserProfile
        fields = ('website', 'picture')


class WebsiteForm(forms.ModelForm):
    class Meta:
        model = RatingWebsite
        fields = ('name', 'url', 'thumbnail', 'description',)


class RatingForm(forms.ModelForm):
    user = forms.ModelChoiceField(widget=forms.HiddenInput(), required=False, queryset=User.objects.all())
    website = forms.ModelChoiceField(widget=forms.HiddenInput(), required=False, queryset=RatingWebsite.objects.all())

    class Meta:
        model = Rating
        fields = ('rating','user','website',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('title', 'text',)
