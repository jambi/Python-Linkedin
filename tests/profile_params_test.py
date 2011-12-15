import unittest
from linkedin.params import *

class ProfileParamsTest(unittest.TestCase):
    
    def setUp(self):
        self.params = Profile()
    
    def test_default_profile(self):
        self._assert_url_for_api("~")
        
    def test_profile_for_id(self):
        self.params.set_id("123")
        self._assert_url_for_api("id=123")
        
    def test_profile_for_id_number(self):
        self.params.set_id(444)
        self._assert_url_for_api("id=444")
        
    def test_profile_for_id_encoded(self):
        self.params.set_id("Ab#/ss$")
        self._assert_url_for_api("id=Ab%23%2Fss%24")
        
    def test_profile_for_url(self):
        self.params.set_url("url")
        self._assert_url_for_api("url=url")
        
    def test_profile_for_url_encoded(self):
        self.params.set_url("http://www.linkedin.com/my_profile")
        self._assert_url_for_api("url=http%3A%2F%2Fwww.linkedin.com%2Fmy_profile")
        
    def _assert_url_for_api(self, expected):
        self.assertEquals(expected, self.params.get_url_for_api())