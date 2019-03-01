from django.contrib import admin
from webapp.models import RatingWebsite, Rating, Comment

class RatingWebsiteAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}

admin.site.register(RatingWebsite, RatingWebsiteAdmin)
admin.site.register(Rating)
admin.site.register(Comment)