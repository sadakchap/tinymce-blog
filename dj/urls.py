from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from django.contrib.auth import views as auth_views

sitemaps = {
    'posts': PostSitemap,
}

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.HomePage.as_view(),name='index'),
    path('about/',views.AboutPage.as_view(),name='about'),
    path('blog/',include('blog.urls')),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('tinymce/',include('tinymce.urls')),
    path('sitemaps.xml',sitemap,{'sitemaps':sitemaps},name='django.contrib.sitemaps.views.sitemap'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
