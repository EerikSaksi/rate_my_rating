from webapp.models import RatingWebsite
from django.urls import resolve, Resolver404
from django.test import TestCase
from population_script import populate
from django.urls import resolve, Resolver404,reverse



class RatingWebsiteTestCase(TestCase):
    def test_all_urls_are_mapped(self):
        allSlugs=RatingWebsite.objects.all().values_list('slug', flat=True)
        for slug in allSlugs:
            try:
                resolve("websites/"+slug)
            except:
                #if there is a url that doesn't map then fail the test
                print("Url with %s slug isn't mapped."%slug)
                self.assertTrue(False)
        #if all urls passed then the test is passed
        print("All urls are mapped")
        self.assertTrue(True)

class ServerResponseTestCase(TestCase):
    def test_index_uses_correct_template(self):
        response = self.client.get(reverse('about'))
        self.assertEquals(response.status_code, 200)

    def test_everyone_is_acknowledged(self):
        response = self.client.get(reverse('about'))
        self.assertIn("Haowen Li", response.content.decode())
        self.assertIn("Eerik Saksi", response.content.decode())
        self.assertIn("David Jasek", response.content.decode())
        self.assertIn("Mahmood Khalil", response.content.decode())

    def test_index_contains_all_links(self):
        response = self.client.get(reverse('index'))
        self.assertIn("href="/"Home")









    











