from django.shortcuts import render, redirect, get_object_or_404
from webapp.models import RatingWebsite, Rating, Comment, UserProfile
from webapp.forms import UserForm, UserProfileForm, WebsiteForm, CommentForm, UserEditForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.utils.timezone import now

def index(request):
    # 5 websites with best average rating
    top_websites = RatingWebsite.objects.all()
    top_websites = sorted(top_websites, key=lambda t: -t.average_rating())[:5]

    # 5 most recent websites
    new_websites = RatingWebsite.objects.all().order_by('-published')[:5]

    # 5 best rated websites out of 15 most recent websites
    trending_websites = RatingWebsite.objects.order_by('-published')[:15]
    trending_websites = sorted(trending_websites, key=lambda t: -t.average_rating())[:5]

    context_dict = {'top_websites': top_websites, 'new_websites': new_websites, 'trending_websites': trending_websites}
    return render(request, 'webapp/index.html', context=context_dict)

def about(request):
    return render(request, 'webapp/about.html')

def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Account successfully created!')
            return redirect('my_account')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'webapp/register.html', context_dict)

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def my_account(request):
    average_rating = 0.0
    # all website created by current user
    websites = request.user.ratingwebsite_set.all().order_by('-published')

    # get overall average rating of all user's websites
    if len(websites) > 0:
        for website in websites:
            average_rating += website.average_rating()
        average_rating /= len(websites)

    context_dict = {'websites': websites, 'average_rating': float("{0:.2f}".format(average_rating))}
    return render(request, 'webapp/my-account.html', context_dict)

@login_required
def my_account_edit(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        # change password
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('my_account_edit')

        # update user details
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

    context_dict = {'password_form': password_form, 'profile_form': profile_form, 'user_form': user_form}
    return render(request, 'webapp/my-account-edit.html', context_dict)

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

    context_dict = {'form': form}
    return render(request, 'webapp/my-account-upload.html', context_dict)

def show_websites(request):
    search = request.GET.get('search', '')

    if search == '':
        websites = RatingWebsite.objects.all()
    else:
        websites = RatingWebsite.objects.filter(name__contains=search)

    # sort websites by average rating
    websites = sorted(websites, key=lambda t: -t.average_rating())

    context_dict = {'websites': websites}
    return render(request, 'webapp/websites.html', context_dict)

def website_detail(request, website_slug):
    website = RatingWebsite.objects.get(slug=website_slug)
    ratings = Rating.objects.filter(website=website).order_by('-published')[:5]
    comments = Comment.objects.filter(website=website).order_by('-published')

    current_rating = 0

    if request.user.is_authenticated:
        # try to get the instance of user's rating for this website
        try:
            current_rating = Rating.objects.get(user=request.user, website=website).rating
        except Rating.DoesNotExist:
            pass

    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.website = website

            comment.save()
            messages.success(request, 'Comment saved.')
            return redirect('website_detail', website_slug)

    elif request.user.is_authenticated:
        comment_form = CommentForm()
    else:
        comment_form = None

    context_dict = {'website': website, 'ratings': ratings, 'comments': comments,
                    'current_rating': current_rating, 'comment_form': comment_form}
    return render(request, 'webapp/website_details.html', context_dict)

@login_required
def website_edit(request, website_slug):
    website = get_object_or_404(RatingWebsite, slug=website_slug, owner=request.user)

    if request.method == 'POST':
        form = WebsiteForm(request.POST, request.FILES, instance=website)
        if form.is_valid():
            website = form.save()
            messages.success(request, 'Website updated')

            return redirect('website_edit', website.slug)
    else:
        form = WebsiteForm(instance=website)

    context_dict = {'website': website, 'form': form}
    return render(request, 'webapp/website_edit.html', context_dict)

@login_required
def website_update_rating(request, website_slug):
    website = get_object_or_404(RatingWebsite, slug=website_slug)
    if request.method == 'POST':
        new_rating = request.POST.get('rating', None)

        if new_rating is not None:
            if request.user != website.owner:
                rating = Rating.objects.get_or_create(website=website, user=request.user)[0]
                rating.rating = new_rating
                rating.published = now()
                rating.save()

                response = {'message': 'success', 'average_rating': website.average_rating(), 'ratings': []}
                ratings = Rating.objects.filter(website=website).order_by('-published')[:5]
                for rating in ratings:
                    response['ratings'].append({'rating': rating.rating, 'user': rating.user.username})
                return JsonResponse(response)
    return JsonResponse({'message': 'error'})


