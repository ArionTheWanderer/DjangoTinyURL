import hashlib
import random
import string

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.conf import settings

from .models import Url


def index(request):
    return render(request, 'apptinyurl/index.html')


def redirect_to_site(request, short_url):
    print(short_url)
    url = get_object_or_404(Url, pk=short_url)
    url.clicks_number += 1
    url.save()
    return HttpResponseRedirect(url.long_url)


def create_short_url(url: str):
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    while True:
        salt = ''.join(random.choice(chars) for x in range(7))
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
    url = request.POST.get('url')
    if url != '':
        short_url = create_short_url(url)
        new_url_object = Url(long_url=url, short_url=short_url)
        new_url_object.save()
        response_data = settings.BASE_URL + "/" + short_url
        return render(request, 'apptinyurl/index.html', {'short_url': response_data})
    return render(request, 'apptinyurl/index.html', {'error_message': 'Enter url!'})
