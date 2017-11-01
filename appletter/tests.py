import unittest
from views import create_letter
from appletter.utils import *

class CreateLetterTestCase(unittest.TestCase):
    def test_bad_username(self):
        """hello view actually tells 'Hello'."""
        # Setup.
        request = 'fake request'
        username = 'dlslsgjfjkgdkfljglkdfjg'
        # Run.
        response = create_letter(request, username)
        # Check.
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, u"Haven't found profile")

    def test_empty_profile(self):
        """hello view actually tells 'Hello'."""
        # Setup.
        request = 'fake request'
        username = 'emptyprofile31415'
        # Run.
        response = create_letter(request, username)
        # Check.
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content, u"Not enough publicatins: 0")

    def test_private_profile(self):
        """hello view actually tells 'Hello'."""
        # Setup.
        request = 'fake request'
        username = 'indiesashka'
        # Run.
        response = create_letter(request, username)
        # Check.
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content, u"Profile is private")

    def test_open_profile(self):
        """hello view actually tells 'Hello'."""
        # Setup.
        request = 'fake request'
        username = 'reachoutfaith'
        # Run.
        response = create_letter(request, username)
        # Check.
        self.assertEqual(response.status_code, 200)

class UtilsTestCase(unittest.TestCase):
	def test_media_count_full(self):
		self.assertEqual(len(get_all_media(str(1545875210))), 342)

	def test_media_count_less_than_step(self):
		self.assertEqual(len(get_all_media(str(5781823989))), 10)

	def test_media_no_id(self):
		self.assertEqual(get_all_media(str(-1)), None)