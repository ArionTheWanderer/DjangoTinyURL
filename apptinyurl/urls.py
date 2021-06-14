from django.urls import path

from . import views

app_name = 'tinyurl'
urlpatterns = [
    path('shorten/', views.shorten_url, name="shorten"),
    path('<str:short_url>/', views.redirect_to_site, name='redirect'),
    path('', views.index, name='index')
]
