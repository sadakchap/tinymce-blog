from django.urls import path
from . import views
from .feeds import LatestPostFeed

app_name = 'blog'

urlpatterns = [
	path('',views.post_list,name='post-list'),
	path('tag/<slug:tag_slug>/',views.post_list,name='post-list'),
	path('detail/<slug:slug>/',views.post_detail,name='detail'),
	path('share/<slug:slug>/',views.post_share,name='share'),
	path('feed/',LatestPostFeed(),name='post-feed'),
]
