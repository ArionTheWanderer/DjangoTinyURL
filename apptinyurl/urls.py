from django.urls import path

from . import views

app_name = 'tinyurl'
urlpatterns = [
    path('shorten/', views.shorten_url, name="shorten"),
    path('all-links/', views.AllLinksView.as_view(), name="all-links"),
    path('all-links/<slug:short_url>/delete/', views.delete_url, name="delete-link"),
    path('<slug:short_url>/', views.redirect_to_site, name='redirect'),
    path('', views.index, name='index')
]
