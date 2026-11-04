from django.test import TestCase
from django.urls import reverse


class GetCookieTestCase(TestCase):
    def test_get_cookie(self):
        result = self.client.get(reverse('myauth:get_cookie'))
        self.assertContains(result, 'Cookie value')


class FooBarTestCase(TestCase):
    def test_foobar(self):
        response = self.client.get(reverse('myauth:foo_bar'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        data = {'foo': 'bar', 'spam': 'eggs'}
        self.assertJSONEqual(response.content, data)
