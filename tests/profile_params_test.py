import unittest
from linkedin.params import *
import re

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
    
    def test_id_comes_last(self):
        self.params.set_id(123).set_url("http://sdfsdf").me().set_id("1")
        self._assert_url_for_api("id=1")
        
    def test_me_comes_last(self):
        self.params.set_url("http://sss.com").set_id("DVC").me()
        self._assert_url_for_api("~")
        
    def test_url_comes_last(self):
        self.params.set_id("tt5").me().set_url("aaa")
        self._assert_url_for_api("url=aaa")
        
    def test_public_no_fields(self):
        self.params.public()
        self._assert_url_for_api("~:public")
        self.params.set_id("222")
        self._assert_url_for_api("id=222:public")
        
    def test_turning_public_to_private(self):
        self.params.set_url("eee").public().private()
        self._assert_url_for_api("url=eee")
        
    def test_some_simple_fields(self):
        expected_fields = sorted(["summary", "first-name", "headline"])
        self.params.add_summary().add_first_name().add_headline()
        self.assertEquals(expected_fields, self._get_fields_for_fields("~"))
        
    def test_some_simple_fields_with_id(self):
        expected_fields = sorted(["last-name", "public-profile-url"])
        self.params.add_last_name().add_public_profile_url()
        self.params.set_id(1)
        self.assertEquals(expected_fields, self._get_fields_for_fields("id=1"))
        
    def _assert_url_for_api(self, expected):
        self.assertEquals(expected, self.params.get_url_for_api())
        
    def _assert_url_for_api_matches(self, expected_re):
        url = self.params.get_url_for_api()
        self.assertTrue(re.match(expected_re, url),
                        "{url} should match {re}".format(url=url, re=expected_re))
    
    def _get_fields_for_fields(self, field):
        url = self.params.get_url_for_api()
        exp = field + ":\((.*)\)"
        result = re.search(exp, url)
        self.assertTrue(result,
            "{field} should have parameters in url: {url}".format(field=field, url=url))
        
        return sorted(result.group(1).split(","))
        