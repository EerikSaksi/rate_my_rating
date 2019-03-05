from django.shortcuts import render
from webapp.models import RatingWebsite, Rating
from datetime import datetime

def index(request):
    # arbitrary value for how how many likes you have to have to get to trending, otherwise trending is new
    minLikesTrending = 2

    # set a minimum rating for website. Otherwise controversial ratings with lots of bad websites might be top.
    # also arbitrary and subject to change
    minRatingTop = 0

    # key: website
    # value= a list L such that L[0] stores the total number of ratings, and L[1] stores the average rating of
    # this website. This dict will temporarily store a list of ratings in L[0] in order to find the top and trending
    # websites.
    websiteRatingsDict = {}

    for rating in Rating.objects.all():
        #if the website is not inside initialize the list and the average
        if (rating.website not in websiteRatingsDict):
            websiteRatingsDict[rating.website]=[[],0]

        #add the value of this rating ot the list
        websiteRatingsDict[rating.website][0].append(rating.rating)


    #this will store the website objects of at most 5 websites that are above the minimum threshold and
    #have the most ratings
    topWebsites = []

    for website in websiteRatingsDict:

        # get the list of ratings of the current website
        currentRatingList = websiteRatingsDict[website][0]

        # calculate its average rating
        averageRating = 0
        for rating in currentRatingList:
            averageRating += rating
        averageRating = averageRating / float(len(currentRatingList))


        #store the average rating in the dict
        websiteRatingsDict[website][1]=averageRating

        # if the rating is high enough, see if it belongs in the top 5 websites.
        if (averageRating > minRatingTop):
            index = 0
            # iterate the list in ascending order, until the number of ratings at index is larger
            # than the number of ratings in currentRatingList
            while (index < len(topWebsites) and len(websiteRatingsDict.get(topWebsites[index])) < len(currentRatingList)):
                index += 1

            # if we don't have five elements insert it where it belongs, even if it is
            # the smallest element
            if (len(topWebsites) < 5):
                topWebsites.insert(index, website)

            # if we do have 5 elements, if this isn't the smallest in topWebsites,
            # insert it where it belongs and pop the smallest.
            elif (index != 5):
                topWebsites.insert(index, website)
                topWebsites.pop(0)





    newWebsites=RatingWebsite.objects.order_by('-published')[:5]

    #iterate through the websites, storing their total number of ratings and average rating
    topWebsitesMeta={}
    for website in topWebsites:
        topWebsitesMeta[website]=websiteRatingsDict[website]
    newWebsitesMeta={}
    for website in newWebsites:
        newWebsitesMeta[website] = websiteRatingsDict[website]
    s


    context_dict = {'topWebsites': topWebsitesMeta, 'newWebsites':newWebsitesMeta,'trendingWebsites':trendingWebsitesMeta}


    return render(request, 'index.html', context=context_dict)
