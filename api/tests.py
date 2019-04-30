from django.test import TestCase

from api.views import stops


class ApiTests(TestCase):

    def test_get_stops(self):
        response = stops(None)

        self.assertEqual(200, response.status_code)
        # TODO: why is b contained before the array?
        # self.assertEqual('b[]', response.content)
