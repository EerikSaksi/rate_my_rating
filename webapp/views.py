from django.shortcuts import render, redirect, get_object_or_404
from webapp.models import RatingWebsite, Rating
from webapp.forms import UserForm, UserProfileForm, WebsiteForm, RatingForm, CommentForm, UserEditForm
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from webapp.models import UserProfile

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

    for website in RatingWebsite.objects.all():
        websiteRatingsDict[website] = [[],0]
        for rating in website.rating_set.all():
             websiteRatingsDict[website][0].append(rating.rating)

    #this will store the website objects of at most 5 websites that are above the minimum threshold and
    #have the most ratings
    topWebsites = []


    for website in websiteRatingsDict:

        # get the list of ratings of the current website
        currentRatingList = websiteRatingsDict[website][0]

        # calculate its average rating
        averageRating = 0
        if len(currentRatingList) > 0:
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

def register(request):

	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			profile.save()
			registered = True
		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request,
				'register.html',
				{'user_form': user_form,
				'profile_form': profile_form,
				'registered': registered})

def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse("Something goes wrong.")
		else:
			print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied.")
	else:
		return render(request, 'login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def my_account(request):
    current_user = request.user
    context_dict = {'current_user': current_user}

    average_rating = 0.0
    websites = current_user.ratingwebsite_set.all().order_by('-published')
    num_websites = len(websites)
    if num_websites > 0:
        for website in websites:
            average_rating += website.average_rating()
        average_rating /= len(websites)
    context_dict['average_rating'] = average_rating
    context_dict['websites'] = websites
    context_dict['num_websites'] = num_websites

    return render(request, 'my-account.html', context_dict)

@login_required
def my_account_edit(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('my_account_edit')

        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, 'Account details successfully updated!')
            return redirect('my_account_edit')
            
    else:
        password_form = PasswordChangeForm(request.user)
        profile_form = UserProfileForm(instance=profile)
        user_form = UserEditForm(instance=request.user)
    return render(request, 'my-account-edit.html', {'password_form': password_form, 'profile_form': profile_form, 'user_form': user_form})

@login_required
def my_account_upload(request):
    if request.method == 'POST':
        form = WebsiteForm(request.POST, request.FILES)
        if form.is_valid():
            website = form.save(commit=False)
            website.owner = request.user
            website.save()

            messages.success(request, 'Website successfully uploaded.')
            return redirect('my_account')
    else:
        form = WebsiteForm()
    return render(request, 'my-account-upload.html', {'form': form})

def show_websites(request):
    search = request.GET.get('search', '')
    if search == '':
        websites = RatingWebsite.objects.all()
    else:
        websites = RatingWebsite.objects.filter(name__contains=search)

    # sort websites by average rating
    websites = sorted(websites, key=lambda t: -t.average_rating())

    return render(request, 'websites.html', {'websites': websites})

def website_detail(request, website_slug):
    website = RatingWebsite.objects.get(slug=website_slug)
    ratings = Rating.objects.filter(website=website).order_by('-published')[:5]

    logged_in = request.user.is_authenticated

    if logged_in:
        # try to get the instance of user's rating for this website
        try:
            current_rating = instance=Rating.objects.get(user=request.user, website=website)
        except Rating.DoesNotExist:
            current_rating = None

    if request.method == 'POST' and logged_in:
        form = RatingForm(request.POST, instance=current_rating)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.website = website

            if rating.user != rating.website.owner:
                rating.save()
                messages.success(request, 'Rating saved.')
            else:
                messages.error(request, 'You cannot rate your own website.')

            return redirect('website_detail', website_slug)
    elif logged_in:
        form = RatingForm(instance=current_rating)
    else:
        form = None

    return render(request, 'website_details.html', {'website': website, 'ratings': ratings, 'form': form})

@login_required
def website_edit(request, website_slug):
    website = get_object_or_404(RatingWebsite, slug=website_slug, owner=request.user)

    if request.method == 'POST':
        form = WebsiteForm(request.POST, request.FILES, instance=website)
        if form.is_valid():
            rating = form.save()
            messages.success(request, 'Website updated')

            return redirect('website_edit', website_slug)
    else:
        form = WebsiteForm(instance=website)

    return render(request, 'website_edit.html', {'website': website, 'form': form})
