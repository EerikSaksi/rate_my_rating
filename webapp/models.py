from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class RatingWebsite(models.Model):
    name = models.CharField(max_length=30, unique=True)
    url = models.URLField(unique=True)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    desciption = models.TextField()

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(RatingWebsite, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Rating(models.Model):
    website = models.ForeignKey(RatingWebsite, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    rating = models.IntegerField()

    def __str__(self):
        return self.user.first_name + ' - ' + self.website.name + ' (' + self.rating + ')'


class Comment(models.Model):
    website = models.ForeignKey(RatingWebsite, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=30)
    text = models.TextField()

    def __str__(self):
        return self.user.first_name + ' - ' + self.website.name + ' (' + self.title + ')'
