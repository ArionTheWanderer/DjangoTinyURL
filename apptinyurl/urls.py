from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'tinyurl'
urlpatterns = [
    path('shorten/', views.shorten_url, name="shorten"),
    path('<slug:short_url>/', views.redirect_to_site, name='redirect'),
    path('', views.index, name='index')
]
