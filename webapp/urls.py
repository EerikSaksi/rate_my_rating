from django.conf.urls import url
from django.contrib.auth.views import LoginView

from webapp import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^login/$', LoginView.as_view(template_name='webapp/login.html'), name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^my-account/$', views.my_account, name='my_account'),
    url(r'^my-account/edit/$', views.my_account_edit, name='my_account_edit'),
    url(r'^my-account/upload/$', views.my_account_upload, name='my_account_upload'),
    url(r'^websites/$', views.show_websites, name='websites'),
    url(r'^websites/(?P<website_slug>[\w\-]+)/$', views.website_detail, name='website_detail'),
    url(r'^websites/(?P<website_slug>[\w\-]+)/edit/$', views.website_edit, name='website_edit'),
    url(r'^websites/(?P<website_slug>[\w\-]+)/update-rating$', views.website_update_rating, name='website_update_rating'),
]
