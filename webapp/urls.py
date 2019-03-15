from django.conf.urls import url

from webapp import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^my-account/$', views.my_account, name='my_account'),
    url(r'^my-account/edit/$', views.my_account_edit, name='my_account_edit'),
    url(r'^my-account/upload/$', views.my_account_upload, name='my_account_upload'),
    url(r'^websites/$', views.show_websites, name='websites'),
    url(r'^websites/(?P<website_slug>[\w\-]+)/$', views.website_detail, name='website_detail'),
    url(r'^websites/(?P<website_slug>[\w\-]+)/edit/$', views.website_edit, name='website_edit'),
]
