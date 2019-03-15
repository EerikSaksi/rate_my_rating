from django import forms
from django.contrib.auth.models import User
from webapp.models import UserProfile, RatingWebsite, Rating, Comment

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password', 'email', 'first_name', 'last_name',)

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
