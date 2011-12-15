'''
Created on Aug 31, 2011

@author: Iftach
'''

from tests import *
from linkedin import linkedin

class LinkedInRequestTest(LinkedInTestBase):

    def test_request_token(self):
        self._test_request_token(False)
        
    def test_request_token_gae(self):
        self._init_gae()
        self._test_request_token(True)
        
    def _test_request_token(self, gae):
        "request_token doesn't raise error"
        api = linkedin.LinkedIn(API_KEY, SECRET_KEY, RETURN_URL, gae)
        api.request_token()

if __name__ == "__main__":
    unittest.main()