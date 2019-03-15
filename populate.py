import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'rate_my_rating.settings')

import django
django.setup()
from webapp.models import RatingWebsite, Rating, Comment, UserProfile
from django.contrib.auth.models import User
from django.utils.timezone import get_current_timezone
from datetime import datetime

def add_user(username, email, password):
    u = User.objects.get_or_create(username=username)[0]
    u.email = email
    u.password = password

    u.save()
    
    up = UserProfile.objects.get_or_create(user=u)[0]
    up.save()
    return u

def add_website(name, url, description, owner, published='', thumbnail=''):
    owner = User.objects.get(username=owner)
    w = RatingWebsite.objects.get_or_create(name=name, owner=owner)[0]
    w.url = url
    w.description = description
    if published != '':
        tz = get_current_timezone()
        w.published = tz.localize(datetime.strptime(published, '%Y/%m/%d %H:%M'))
    if thumbnail != '':
        w.thumbnail = thumbnail
    
    w.save()
    return w

def add_rating(rating, user, website, published=''):
    user = User.objects.get(username=user)
    website = RatingWebsite.objects.get(name=website)

    r = Rating.objects.get_or_create(user=user, website=website)[0]
    r.rating = rating
    if published != '':
        tz = get_current_timezone()
        r.published = tz.localize(datetime.strptime(published, '%Y/%m/%d %H:%M'))

    r.save()
    return r

def add_comment(title, text, user, website, published=''):
    user = User.objects.get(username=user)
    website = RatingWebsite.objects.get(name=website)
    
    c = Comment.objects.get_or_create(user=user, website=website)[0]
    c.title = title
    c.text = text
    if published != '':
        tz = get_current_timezone()
        c.published = tz.localize(datetime.strptime(published, '%Y/%m/%d %H:%M'))

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
         'owner': 'ILovePets365',
         'thumbnail': 'thumbnails/placeholder.png',
         'published': '2018/12/24 12:00'},
        {'name': 'Rate my floss',
         'url': 'http://ratemyfloss.com',
         'description': 'Rating website for all epic gamers out there. Upload your floss videos and get instant feedback from our great community!',
         'owner': 'WEBSITElover',
         'thumbnail': 'thumbnails/placeholder.png',
         'published': '2017/06/09 22:15'},
        {'name': 'Rate me from behind',
         'url': 'http://ratemefrombehind.org',
         'description': 'Browse thousands of hip thrusts videos and rate them. Our videos range from total beginners to absolute beasts and the best part? You can even upload your home made hip thrust videos. So what are you waiting for? (Family friendly content only!!!)',
         'owner': 'WEBSITElover',
         'thumbnail': 'thumbnails/placeholder.png',
         'published': '2019/03/04 14:00'},
        {'name': 'Rate my populate script',
         'url': 'http://populatemyrate.co.uk',
         'description': 'Rate populate scripts for wad2 projects.',
         'owner': 'WEBSITElover',
         'thumbnail': 'thumbnails/placeholder.png',
         'published': ''},
        {'name': 'Rate my angle grinder',
         'url': 'http://ratemygrinder.com',
         'description': 'Website for all fans of angle grinders to share and rate their angle grinders.',
         'owner': 'WEBSITElover',
         'thumbnail': 'thumbnails/placeholder.png',
         'published': ''},
        {'name': 'Rate my siege weapon',
         'url': 'http://trebuchetrulez.com',
         'description': 'Share your superior siege weapons with your friends and family. No catapults allowed!!!',
         'owner': 'xxxRATINGGURUxxx',
         'thumbnail': 'thumbnails/placeholder.png',
         'published': ''},
        {'name': 'Generic website',
         'url': 'http://generic.com',
         'description': 'Ipsum sint officia consectetur labore velit amet fugiat amet. Cupidatat fugiat incididunt nisi cupidatat culpa minim veniam. Deserunt amet ex consequat culpa ad esse. Anim nisi consequat aliqua cupidatat magna ipsum ullamco. Dolore et non deserunt reprehenderit et cillum sit mollit amet magna.',
         'owner': 'WEBSITElover',
         'thumbnail': 'thumbnails/placeholder.png',
         'published': ''},
        {'name': 'Generic website 2',
         'url': 'http://generic2.com',
         'description': 'Dolor proident non aute in sint id sunt consequat et aliquip mollit magna.',
         'owner': 'WEBSITElover',
         'thumbnail': 'thumbnails/placeholder.png',
         'published': ''},
        {'name': 'Rate my etruscan boar vessel 600-500 bc ceramic',
         'url': 'http://etruscan-boar-vessel-600-500-bc-ceramic.com',
         'description': 'The best site for etruscan boar vessel 600-500 bc ceramic lovers. Come and share your etruscan boar vessel 600-500 bc ceramic and rate the etruscan boar vessel 600-500 bc ceramic.',
         'owner': 'WEBSITElover',
         'thumbnail': 'thumbnails/placeholder.png',
         'published': ''},

    ]

    ratings = [
        {'rating': 0,
         'user': 'Hater_of_the_Internet',
         'website': 'Rate my pet',
         'published': '2019/03/01 14:00'},
        {'rating': 0,
         'user': 'Hater_of_the_Internet',
         'website': 'Rate my floss',
         'published': '2019/03/02 14:00'},
        {'rating': 0,
         'user': 'Hater_of_the_Internet',
         'website': 'Rate me from behind',
         'published': '2019/03/03 14:00'},
        {'rating': 4,
         'user': 'WEBSITElover',
         'website': 'Rate my pet',
         'published': '2019/03/04 12:00'},
        {'rating': 3,
         'user': 'xxxRATINGGURUxxx',
         'website': 'Rate my pet',
         'published': '2019/02/15 14:00'},
        {'rating': 2,
         'user': 'xxxRATINGGURUxxx',
         'website': 'Rate my floss',
         'published': '2018/12/31 14:00'},
        {'rating': 5,
         'user': 'rating_master',
         'website': 'Rate me from behind',
         'published': '2019/04/20 04:20'},
        {'rating': 2,
         'user': 'rating_master',
         'website': 'Rate my floss',
         'published': '2019/01/22 14:00'},
        {'rating': 1,
         'user': 'ILovePets365',
         'website': 'Rate me from behind',
         'published': '2019/03/04 11:00'},
        {'rating': 4,
         'user': 'ILovePets365',
         'website': 'Rate my floss',
         'published': '2019/03/04 10:00'},
        {'rating': 5,
         'user': 'ILovePets365',
         'website': 'Rate my populate script',
         'published': ''},
        {'rating': 5,
         'user': 'rating_master',
         'website': 'Rate my populate script',
         'published': ''},
        {'rating': 5,
         'user': 'xxxRATINGGURUxxx',
         'website': 'Rate my populate script',
         'published': ''},
        {'rating': 4,
         'user': 'ILovePets365',
         'website': 'Rate my angle grinder',
         'published': ''},
        {'rating': 4,
         'user': 'rating_master',
         'website': 'Rate my angle grinder',
         'published': ''},
        {'rating': 4,
         'user': 'xxxRATINGGURUxxx',
         'website': 'Rate my angle grinder',
         'published': ''},
        {'rating': 5,
         'user': 'ILovePets365',
         'website': 'Rate my siege weapon',
         'published': ''},
        {'rating': 5,
         'user': 'ILovePets365',
         'website': 'Rate my etruscan boar vessel 600-500 bc ceramic',
         'published': ''},
    ]

    comments = [
        {'title': 'I hate this website',
         'text': 'This website sucks!!!',
         'user': 'Hater_of_the_Internet',
         'website': 'Rate my pet',
         'published': '2018/03/04 10:00'},
        {'title': 'No thanks',
         'text': 'My mom creates better websites than this.',
         'user': 'Hater_of_the_Internet',
         'website': 'Rate my floss',
         'published': '2019/03/04 10:00'},
        {'title': 'Nice design',
         'text': 'I really like the design of this website.',
         'user': 'WEBSITElover',
         'website': 'Rate my pet',
         'published': '2019/02/04 15:00'},
        {'title': 'Great idea!',
         'text': 'This website helped me improve my exercises in few easy steps. Personal trainers hate me!!!!',
         'user': 'rating_master',
         'website': 'Rate me from behind',
         'published': '2018/12/23 05:00'},
        {'title': 'I prefer minecraft',
         'text': 'My dead grandma can floss better than these fortnite kids...',
         'user': 'rating_master',
         'website': 'Rate my floss',
         'published': '2018/12/04 10:00'},
        {'title': 'Not what I expected',
         'text': 'I expected NSFW content, but instead got just bunch of weird exercise videos.',
         'user': 'ILovePets365',
         'website': 'Rate me from behind',
         'published': '2019/02/04 13:00'},
        {'title': 'Great website',
         'text': 'I really like to floss LMAO ;). I\'ll improve my rating to 5, if you rate me back ;) ;).',
         'user': 'ILovePets365',
         'website': 'Rate my floss',
         'published': '2019/01/15 10:00'},
        {'title': 'The best',
         'text': 'I have never seen better populate script!!!',
         'user': 'ILovePets365',
         'website': 'Rate my populate script',
         'published': ''},
        {'title': 'Yay',
         'text': 'This populate script is awesome',
         'user': 'rating_master',
         'website': 'Rate my populate script',
         'published': ''},
        {'title': 'Wow',
         'text': 'I have a crippling depression.',
         'user': 'xxxRATINGGURUxxx',
         'website': 'Rate my populate script',
         'published': ''},
        {'title': 'Great website',
         'text': 'This is my first website guys. Pls be gentle.',
         'user': 'xxxRATINGGURUxxx',
         'website': 'Rate my siege weapon',
         'published': ''},
        {'title': 'etruscan boar vessel 600-500 bc ceramic',
         'text': 'I love etruscan boar vessel 600-500 bc ceramic! etruscan boar vessel 600-500 bc ceramic is my favorite thing. I rate this 5 etruscan boar vessel 600-500 bc ceramic out of 7 etruscan boar vessel 600-500 bc ceramic.',
         'user': 'xxxRATINGGURUxxx',
         'website': 'Rate my etruscan boar vessel 600-500 bc ceramic',
         'published': ''},
    ]

    for user in users:
        add_user(user['username'], user['email'], user['password'])
        print('Added user:', user['username'])

    for website in websites:
        add_website(website['name'], website['url'], website['description'], website['owner'], website['published'], website['thumbnail'])
        print('Added website:', website['name'])

    for rating in ratings:
        add_rating(rating['rating'], rating['user'], rating['website'], rating['published'])
        print('Added rating:', rating['user'], rating['website'])

    for comment in comments:
        add_comment(comment['title'], comment['text'], comment['user'], comment['website'], comment['published'])
        print('Added comment:', comment['user'], comment['website'])

if __name__ == '__main__':
    print("Starting population script...")
    populate()