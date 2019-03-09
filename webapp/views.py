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
            #websiteRatingsDict[topWebsites[index]] gives the meta info of the current topWebsite
            #so websiteRatingsDict[topWebsites[index]][0] gives the reviews of this website
            #so len(websiteRatingsDict[topWebsites[index]][0]) gives the number of reviews
            while (index < len(topWebsites) and len(websiteRatingsDict[topWebsites[index]][0]) < len(currentRatingList)):
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


    #trending website is any website that is posted today
    trendingWebsites=RatingWebsite.objects.filter(published=datetime.today())

    #now lets remove the website with the least ratings until we only have 5 left
    while (len(trendingWebsites)>5):
        #assume the smallest to be at zero, and store the length of the list of the reviews
        minimumIndex=0
        minimumLength=len(trendingWebsites[0][0])
        for i in range (1, len(trendingWebsites)):
            #if the length of the list of reviews of this website is smaller than that of the smallest
            if (len(websiteRatingsDict[trendingWebsites[i]][0])<minimumLength):
                minimumLength=websiteRatingsDict[trendingWebsites[i]][0]
                minimumIndex=i
        trendingWebsites.pop(minimumIndex)



    #We want to pass the number of reviews to the templates, and not the reviews themselves. Therefore
    #lets convert the reviews in the dict to the number of reviews

    for website in websiteRatingsDict:
        websiteRatingsDict[website][0]=len(websiteRatingsDict[website][0])

    newWebsites=RatingWebsite.objects.order_by('-published')[:5]

    #iterate through the websites, storing their total number of ratings and average rating in their respective dict
    topWebsitesMeta={}

    #topWebsites stores in ascending order, descending order is neeeded for them to be in correct order

    topWebsites.reverse()
    for website in topWebsites:
        topWebsitesMeta[website]=websiteRatingsDict[website]
    newWebsitesMeta={}
    for website in newWebsites:
        newWebsitesMeta[website] = websiteRatingsDict[website]
    trendingWebsitesMeta={}
    for website in trendingWebsites:
        trendingWebsitesMeta[website]=websiteRatingsDict[website]


    context_dict = {'topWebsites': topWebsitesMeta, 'newWebsites':newWebsitesMeta,'trendingWebsites':trendingWebsitesMeta}


    return render(request, 'index.html', context=context_dict)

def about(request):
    return render(request, 'about.html')
