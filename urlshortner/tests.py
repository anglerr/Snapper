from django.test import TestCase
from urlshortner.models import UrlShortnerModel, DEFAULT_EXPIRY_DAYS
from django.utils import timezone
from django.test import Client
# Create your tests here.


class URLShortenModelTestCase(TestCase):
    def setUp(self):
        UrlShortnerModel.objects.create(short_url="abcdefghij", actual_url="http://localhost.com/xyz123")
        UrlShortnerModel.objects.create(short_url="123456abcd", actual_url="http://localhost.com/abc789")

    def test_Urlshortnerdb_work(self):
        us1 = UrlShortnerModel.objects.get(short_url="abcdefghij")
        us2 = UrlShortnerModel.objects.get(short_url="123456abcd")
        self.assertEqual(us1.actual_url, "http://localhost.com/xyz123")
        self.assertEqual(us2.actual_url, "http://localhost.com/abc789")

    def test_default_expiry(self):
        us1 = UrlShortnerModel.objects.get(short_url="abcdefghij")
        self.assertAlmostEqual((us1.expiry_date - timezone.now()).total_seconds(), DEFAULT_EXPIRY_DAYS*24*60*60,
                               delta=1)


class URLShortenViewsTestCase(TestCase):
    def setUp(self):
        self.url = "http://google.com"
        data1 = dict({"url": self.url})
        self.client = Client()
        self.response = self.client.post(path='/api/shorten_url/', data=data1, content_type='application/json')

    def test_short_url(self):
        self.assertEqual(self.response.status_code, 200)

    def test_response(self):
        self.assertEqual(self.response.data["actual_url"], self.url)

    def test_retrieve_url(self):
        resp = self.client.post(path="/api/get_original_url/", data=dict({"url": self.response.data["short_url"]}),
                                content_type='application/json')
        self.assertEqual(self.url, resp.data["actual_url"])

    def test_redirect(self):
        resp = self.client.get(path=self.response.data["short_url"])
        self.assertEqual(resp.status_code, 301)
