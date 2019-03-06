from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.timezone import now

class RatingWebsite(models.Model):
    name = models.CharField(max_length=30, unique=True)
    url = models.URLField(unique=True)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    description = models.TextField()

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.DateTimeField(default=now)

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(RatingWebsite, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Rating(models.Model):
    website = models.ForeignKey(RatingWebsite, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    rating = models.IntegerField(default=0)
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
