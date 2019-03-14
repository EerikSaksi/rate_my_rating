from django import forms
from django.contrib.auth.models import User
from webapp.models import UserProfile, RatingWebsite, Rating, Comment

class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        #not sure what we gonna have here
        fields = ('website', 'picture')

class WebsiteForm(forms.ModelForm):
    class Meta:
        model = RatingWebsite
        fields = ('name', 'url', 'thumbnail', 'description',)


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('rating',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('title', 'text',)
