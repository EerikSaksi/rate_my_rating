import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'rate_my_rating.settings')

import django
django.setup()
from webapp.models import RatingWebsite, Rating, Comment
from django.contrib.auth.models import User

def add_user(username, email, password):
    u = User.objects.get_or_create(username=username)[0]
    u.email = email
    u.password = password

    u.save()
    return u

def add_website(name, url, description, owner, thumbnail=''):
    owner = User.objects.get(username=owner)
    w = RatingWebsite.objects.get_or_create(name=name, owner=owner)[0]
    w.url = url
    w.description = description
    if thumbnail != '':
        w.thumbnail = thumbnail
    
    w.save()
    return w

def add_rating(rating, user, website):
    user = User.objects.get(username=user)
    website = RatingWebsite.objects.get(name=website)

    r = Rating.objects.get_or_create(user=user, website=website)[0]
    r.rating = rating

    r.save()
    return r

def add_comment(title, text, user, website):
    user = User.objects.get(username=user)
    website = RatingWebsite.objects.get(name=website)
    
    c = Comment.objects.get_or_create(user=user, website=website)[0]
    c.title = title
    c.text = text

    c.save()
    return c

def populate():
    users = [
        {'username': 'ILovePets365',
         'email': 'ilovepets@gmail.com',
         'password': 'petzrulez'},
        {'username': 'rating_master',
         'email': 'masterofratings@yahoo.com',
         'password': 'ratethat'},
        {'username': 'xxxRATINGGURUxxx',
         'email': 'ratingguru@hotmail.co.uk',
         'password': 'sdaf231423*&23'},
        {'username': 'WEBSITElover',
         'email': 'craig@mcdonalds.com',
         'password': 'SELECT*FROMUsers'},
        {'username': 'Hater_of_the_Internet',
         'email': 'hater@gmail.com',
         'password': 'p4ssw0rd'},
         ]

    websites = [
        {'name': 'Rate my pet',
         'url': 'https://www.rate-my-pet.com',
         'description': 'Rating website for all pet lovers, where they can share and rate pictures of their pets.',
         'owner': 'ILovePets365'},
        {'name': 'Rate my floss',
         'url': 'http://ratemyfloss.com',
         'description': 'Rating website for all epic gamers out there. Upload your floss videos and get instant feedback from our great community!',
         'owner': 'WEBSITElover'},
        {'name': 'Rate me from behind',
         'url': 'http://ratemefrombehind.org',
         'description': 'Browse thousands of hip thrusts videos and rate them. Our videos range from total beginners to absolute beasts and the best part? You can even upload your home made hip thrust videos. So what are you waiting for? (Family friendly content only!!!)',
         'owner': 'WEBSITElover'},
    ]

    ratings = [
        {'rating': 0,
         'user': 'Hater_of_the_Internet',
         'website': 'Rate my pet'},
        {'rating': 0,
         'user': 'Hater_of_the_Internet',
         'website': 'Rate my floss'},
        {'rating': 0,
         'user': 'Hater_of_the_Internet',
         'website': 'Rate me from behind'},
        {'rating': 4,
         'user': 'WEBSITElover',
         'website': 'Rate my pet'},
        {'rating': 3,
         'user': 'xxxRATINGGURUxxx',
         'website': 'Rate my pet'},
        {'rating': 2,
         'user': 'xxxRATINGGURUxxx',
         'website': 'Rate my floss'},
        {'rating': 5,
         'user': 'rating_master',
         'website': 'Rate me from behind'},
        {'rating': 2,
         'user': 'rating_master',
         'website': 'Rate my floss'},
        {'rating': 1,
         'user': 'ILovePets365',
         'website': 'Rate me from behind'},
        {'rating': 4,
         'user': 'ILovePets365',
         'website': 'Rate my floss'},
    ]

    comments = [
        {'title': 'I hate this website',
         'text': 'This website sucks!!!',
         'user': 'Hater_of_the_Internet',
         'website': 'Rate my pet'},
        {'title': 'No thanks',
         'text': 'My mom creates better websites than this.',
         'user': 'Hater_of_the_Internet',
         'website': 'Rate my floss'},
        {'title': 'Nice design',
         'text': 'I really like the design of this website.',
         'user': 'WEBSITElover',
         'website': 'Rate my pet'},
        {'title': 'Great idea!',
         'text': 'This website helped me improve my exercises in few easy steps. Personal trainers hate me!!!!',
         'user': 'rating_master',
         'website': 'Rate me from behind'},
        {'title': 'I prefer minecraft',
         'text': 'My dead grandma can floss better than these fortnite kids...',
         'user': 'rating_master',
         'website': 'Rate my floss'},
        {'title': 'Not what I expected',
         'text': 'I expected NSFW content, but instead got just bunch of weird exercise videos.',
         'user': 'ILovePets365',
         'website': 'Rate me from behind'},
        {'title': 'Great website',
         'text': 'I really like to floss LMAO ;). I\'ll improve my rating to 5, if you rate me back ;) ;).',
         'user': 'ILovePets365',
         'website': 'Rate my floss'},
    ]

    for user in users:
        add_user(user['username'], user['email'], user['password'])
        print('Added user:', user['username'])

    for website in websites:
        add_website(website['name'], website['url'], website['description'], website['owner'])
        print('Added website:', website['name'])

    for rating in ratings:
        add_rating(rating['rating'], rating['user'], rating['website'])
        print('Added rating:', rating['user'], rating['website'])

    for comment in comments:
        add_comment(comment['title'], comment['text'], comment['user'], comment['website'])
        print('Added comment:', comment['user'], comment['website'])

if __name__ == '__main__':
    print("Starting population script...")
    populate()