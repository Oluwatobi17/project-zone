from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^about/$', views.about, name='about'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signout/$', views.logout, name='logout'),
    url(r'^edit-profile/$', views.editprofile, name='editprofile'),
    url(r'^forgot-pass/$', views.forgotpass, name='forgotpass'),
    url(r'^comment/(?P<id>[0-9]+)/$', views.commentproject, name='commentproject'),
    url(r'^changepassword/$', views.changepassword, name='changepassword'),
    url(r'^profile/(?P<username>[%&+ \w+ \W+]+)/$', views.profile, name='profile'),
    url(r'^profile/$', views.defaultprofile, name='defaultprofile'),
    url(r'^edit-project/(?P<id>[0-9]+)/$', views.editproject, name='editproject'),
    url(r'^delete-project/(?P<id>[0-9]+)/$', views.deleteproject, name='deleteproject'),
    url(r'^create-project/$', views.addproject, name='addproject'),
    url(r'^projects/(?P<id>[0-9]+)/$', views.project, name='project'),
    url(r'^projects/$', views.defaultproject, name='defaultproject'),
    url(r'^projects/(?P<username>[%&+ \w+ \W+]+)/$', views.projects, name='projects'),
    #
]
