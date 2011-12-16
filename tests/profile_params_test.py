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
        self.assertEquals(expected_fields, self._get_fields_for_field("~"))
        
    def test_some_simple_fields_with_id(self):
        expected_fields = sorted(["last-name", "public-profile-url"])
        self.params.add_last_name().add_public_profile_url()
        self.params.set_id(1)
        self.assertEquals(expected_fields, self._get_fields_for_field("id=1"))
        
    def test_some_simple_fields_public(self):
        self.params.add_main_address().public()
        self._assert_url_for_api("~:public:(main-address)")
        
    def test_complex_field(self):
        self.params.add_location().set_url("qqq")
        self._assert_url_for_api("url=qqq:(location)")
        self.params.add_location(Location().add_country())
        self._assert_url_for_api("url=qqq:(location:(country))")
        self.params.add_location(Location().add_country().add_name())
        expected_fields = sorted(["country", "name"])
        self.assertEquals(expected_fields, self._get_fields_for_field("location"))
        
    def test_all_fields(self):
        expected_fields = sorted(["id",
            "first-name",
            "last-name",
            "headline",
            "distance",
            "current-share",
            "connections",
            "num-connections",
            "num-connections-capped",
            "summary",
            "specialties",
            "proposal-comments",
            "associations",
            "honors",
            "interests",
            "positions",
            "publications",
            "patents",
            "languages",
            "skills",
            "certifications",
            "educations",
            "three_current_positions",
            "three-past-positions",
            "num-recommenders",
            "recommendations-received",
            "phone-numbers",
            "im-accounts",
            "twitter-accounts",
            "date-of-birth",
            "main-address",
            "member-url-resources",
            "picture-url",
            "public-profile-url",
            "site-standard-profile-request",
            "api-public-profile-request",
            "site-public-profile-request",
            "location",
            "relation-to-viewer",
            "api-standard-profile-request"
            ])
        self.params.all()
        self.assertEquals(expected_fields, self._get_fields_for_field("~"))
        
    def test_default(self):
        expected_fields = sorted(["first-name", "last-name", "headline", "site-standard-profile-request"])
        self.params.default()
        self.assertEquals(expected_fields, self._get_fields_for_field("~"))
        
    def _assert_url_for_api(self, expected):
        self.assertEquals(expected, self.params.get_url_for_api())
        
    def _assert_url_for_api_matches(self, expected_re):
        url = self.params.get_url_for_api()
        self.assertTrue(re.match(expected_re, url),
                        "{url} should match {re}".format(url=url, re=expected_re))
    
    def _get_fields_for_field(self, field):
        """
        For example for the field: moshe
        and the url: moshe:(a,b,c)
        returns a sorted list or a,b,c
        """
        url = self.params.get_url_for_api()
        first_index = url.find(field) + len(field) + 2
        last_index = -1
        count = 1
        for index in range(first_index, len(url)):
            if url[index] == ")":
                count -= 1
            elif url[index] == "(":
                count += 1
            if count == 0:
                last_index = index
                break
            
        if last_index == -1:
            self.fail("{field} should have parameters in url: {url}".format(field=field, url=url))
            
        fields_str = url[first_index:last_index]
        
        return sorted(fields_str.split(","))
        