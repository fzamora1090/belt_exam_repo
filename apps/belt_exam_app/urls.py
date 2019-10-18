from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),

    url(r'^wishes$', views.wishes),
    url(r'^newWish$', views.new_wish),

    url(r'^makeWish$', views.make_wish),
    url(r'^wishesEdit/(?P<id>\d+)$', views.wishes_edit),
    url(r'^update/(?P<id>\d+)$', views.update),


    url(r'^addLikedItem/(?P<id>\d+)$', views.add_liked_item),
    url(r'^unlikeItem/(?P<id>\d+)$', views.unlike),
    url(r'^removeItem/(?P<id>\d+)$', views.remove_item),

    url(r'^granted/(?P<id>\d+)$', views.granted),

    url(r'^stats/(?P<id>\d+)$', views.stats),

    url(r'^logout$', views.logout),




]
