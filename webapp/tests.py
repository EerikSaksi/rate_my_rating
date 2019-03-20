from webapp import models
from django.urls import resolve, Resolver404


def each_website_has_correctly_mapped_url():
    ratingWebsiteSlugs=RatingWebsite.objects.all().values_list('slug', flat=True)

    for slug in ratingWebsiteSlugs:
        try:
            resolve("websites/"+slug)
        except Resolver404:
            print("Website with %s slug doesn't map"%(slug))
        else:
            print("Website with %s slug is mapped" %(slug))


def newWebsitesAreOrganized():
    

def test():
    each_website_has_correctly_mapped_url()




test()





