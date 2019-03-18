from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator

class UserProfile(models.Model):
    #Basic attribute neeeded
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username


# method called if the User is created though Google authentication
def create_profile(backend, user, response, *args, **kwargs):
    profile = UserProfile.objects.get_or_create(user=user)[0]
    profile.save()


class RatingWebsite(models.Model):
    name = models.CharField(max_length=30, unique=True)
    url = models.URLField(unique=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True)
    description = models.TextField(blank=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.DateTimeField(default=now)

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(RatingWebsite, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def average_rating(self):
        avg_rating = 0
        ratings = self.rating_set.all()
        if len(ratings) > 0:
            for rating in ratings:
                avg_rating += rating.rating
            avg_rating /= float(len(ratings))

        return avg_rating


class Rating(models.Model):
    website = models.ForeignKey(RatingWebsite, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    SCORE_CHOICES = zip(range(0,6), range(0,6))
    rating = models.IntegerField(choices=SCORE_CHOICES, default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    published = models.DateTimeField(default=now)

    class Meta:
        unique_together = ('website', 'user',)

    def __str__(self):
        return self.user.username + ' - ' + self.website.name + ' (' + str(self.rating) + ')'


class Comment(models.Model):
    website = models.ForeignKey(RatingWebsite, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=30)
    text = models.TextField()
    published = models.DateTimeField(default=now)

    class Meta:
        unique_together = ('website', 'user',)

    def __str__(self):
        return self.user.username + ' - ' + self.website.name + ' (' + self.title + ')'
