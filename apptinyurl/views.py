import hashlib
import random
import string

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.urls import reverse
from django.views import generic

from .models import Url


class AllLinksView(generic.ListView):
    """
    Render 'All links page'
    get_context_data: adds extra context data to a context object
    queryset: defines list of objects to add to a context object
    """

    queryset = Url.objects.all().order_by('-clicks_number')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_url'] = settings.BASE_URL
        return context


def index(request):
    """
    Render index page
    """
    return render(request, 'apptinyurl/index.html')


def redirect_to_site(request, short_url):
    """
    Redirects user to the original site
    :param short_url: short url of the site
    """
    print(short_url)
    url = get_object_or_404(Url, pk=short_url)
    url.clicks_number += 1
    url.save()
    return HttpResponseRedirect(url.long_url)


def create_short_url(url: str):
    """
    Helper function creating a short url from the original
    :param url: input url (original)
    :return: short url without domain
    """
    chars = string.ascii_letters + string.digits
    while True:
        salt = ''.join(random.choice(chars) for _ in range(7))
        hasher = hashlib.md5()
        hasher.update(url.encode())
        hasher.update(salt.encode())
        hexdigest = hasher.hexdigest()
        print(hexdigest)
        short_url = hexdigest[:8]
        print(short_url)
        try:
            Url.objects.get(pk=short_url)
        except Url.DoesNotExist:
            return short_url


def shorten_url(request):
    """
    Calls a helper function to create short url, saves it in DB and returns it to user
    """
    url = request.POST.get('url')
    if url != '':
        short_url = create_short_url(url)
        new_url_object = Url(long_url=url, short_url=short_url)
        new_url_object.save()
        response_short_url = settings.BASE_URL + short_url
        return render(request, 'apptinyurl/index.html',
                      {'short_url': response_short_url, 'long_url': url})
    return render(request, 'apptinyurl/index.html', {'error_message': 'Enter url!'})


def delete_link(request, short_url):
    """
    Delete the selected link from DB
    :param short_url: short url to delete
    """
    try:
        Url.objects.get(pk=short_url).delete()
    except Url.DoesNotExist:
        raise Http404("Url does not exist")
    return HttpResponseRedirect(reverse('tinyurl:all-links'))
