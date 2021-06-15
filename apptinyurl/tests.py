from django.test import TestCase
from django.urls import reverse
from django.conf import settings

from .models import Url

import string
import hashlib
import random


def create_fake_short_url():
    chars = string.ascii_letters + string.digits
    fake_short_url = ''.join(random.choice(chars) for _ in range(settings.SHORT_URL_LENGTH))
    return fake_short_url


def create_short_url(url):
    chars = string.ascii_letters + string.digits
    salt = ''.join(random.choice(chars) for _ in range(settings.SALT_LENGTH))
    hasher = hashlib.md5()
    hasher.update(url.encode())
    hasher.update(salt.encode())
    hexdigest = hasher.hexdigest()
    short_url = hexdigest[:settings.SHORT_URL_LENGTH]
    url_object = Url(short_url=short_url, long_url=url)
    url_object.save()
    return url_object


class IndexViewTests(TestCase):

    def test_get_index_page(self):
        response = self.client.get(reverse('tinyurl:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Shorten your url!")


class RedirectViewTests(TestCase):

    def test_redirect_to_site_from_existing_short_url(self):
        url = 'https://www.google.com/'
        new_url_object = create_short_url(url)
        response = self.client.get(reverse('tinyurl:redirect', args=(new_url_object.short_url,)))
        self.assertEqual(Url.objects.get(pk=new_url_object.short_url).clicks_number, 1)
        self.assertRedirects(response, expected_url=url, fetch_redirect_response=False)
        self.assertEqual(response.url, new_url_object.long_url)

    def test_redirect_to_site_from_not_existing_short_url(self):
        fake_short_url = create_fake_short_url()
        response = self.client.get(settings.BASE_URL + fake_short_url, follow=True)
        self.assertEqual(response.status_code, 404)


class ShortenUrlViewTests(TestCase):

    def test_create_short_url_from_empty_input(self):
        response = self.client.post(reverse('tinyurl:shorten'), {'url': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter properly url!')
        self.assertEqual(response.context['error_message'], 'Enter properly url!')

    def test_create_short_url_from_properly_url(self):
        url = 'https://www.google.com/'
        response = self.client.post(reverse('tinyurl:shorten'), {'url': url})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context['short_url'], [])

    def test_create_short_url_from_not_properly_url(self):
        url = 'http:/www.google,com'
        response = self.client.post(reverse('tinyurl:shorten'), {'url': url})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error_message'], 'Enter properly url!')


class DeleteUrlViewTests(TestCase):

    def test_delete_existing_url(self):
        url = 'https://www.google.com/'
        new_url_object = create_short_url(url)
        response = self.client.post(reverse('tinyurl:delete-link', args=(new_url_object.short_url,)), follow=True)
        is_deleted = False
        try:
            Url.objects.get(pk=new_url_object.short_url)
        except Url.DoesNotExist:
            is_deleted = True
        self.assertEqual(is_deleted, True)
        self.assertEqual(response.status_code, 200)

    def test_delete_not_existing_url(self):
        fake_short_url = create_fake_short_url()
        response = self.client.post(reverse('tinyurl:delete-link', args=(fake_short_url,)))
        self.assertEqual(response.status_code, 404)
