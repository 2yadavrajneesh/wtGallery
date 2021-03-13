from django.contrib import sitemaps
from django.contrib.auth import views as auth
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views
from django.conf import settings
from django.contrib.auth.views import LogoutView

from .views import read_file

urlpatterns = [
    path('', views.index, name='index'),
    path('dashb/', views.dashb, name='dashb'),
    # path('', views.IndexView.as_view(), name='index'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('upload/', views.upload, name='upload'),
    path('video/', views.video, name='video'),
    path('my_account/', views.my_account, name='my_account'),
    path('subscription/', views.subscription, name='subscription'),
    path('image/', views.image, name='image'),
    path('music/', views.music, name='music'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('register/', views.register, name='register'),
    path('search/', views.SearchResultsView.as_view(), name='search'),
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("sitemap.xml", TemplateView.as_view(template_name="sitemap.xml", content_type="text/xml")),
    # Viram Changes

    path('musicviews/', views.save_music_view, name='musicviews'),
    path('countdownloads/', views.count_downloads, name='countdownloads'),
    path('imagelikes/', views.count_likes, name='imagelikes'),
    path('saveviews/', views.save_views, name='saveviews'),
    path('save_video_views/', views.save_video_views, name='save_video_views'),
    path('save_music_views/', views.save_music_view, name='save_music_views'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
