'''
Created on Aug 31, 2011

@author: Iftach
'''

from linkedin.tests import *
from linkedin import linkedin

class LinkedInRequestTest(LinkedInTestBase):

    def test_request_token(self):
        self._test_request_token(False)
        
    def test_request_token_gae(self):
        self._init_gae()
        self._test_request_token(True)
        
    def _test_request_token(self, gae):
        api = linkedin.LinkedIn(API_KEY, SECRET_KEY, RETURN_URL, gae)
        self.assertTrue(api.request_token(), api.get_error())

if __name__ == "__main__":
    unittest.main()