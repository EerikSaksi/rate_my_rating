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
        self.assertIn("href=\"/\">Home",response.content.decode())

    def test_proper_404_response(self):
        #the name is over 30 characters, which is longer than the maximum length, so should be 404
        try:
            resolve("websites/0123456789012345678901234567890123456789")
        except:
            # if there is a url that doesn't map then fail the test
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    











    











