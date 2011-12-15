'''
Created on Aug 31, 2011

@author: Iftach
'''
from tests import *
from linkedin import linkedin


class LinkedInAccessTest(LinkedInTestBase):
    
    def test_access_token_gae(self):
        self._init_gae()
        self._test_access_token(True)
    
    def test_access_token(self):
        self._test_access_token(False)
        
    def _test_access_token(self, gae):
        "Check that it doesn't raise error"
        api = linkedin.LinkedIn(API_KEY, SECRET_KEY, RETURN_URL, gae=gae)
        api.request_token()

        print "----------------"
        print "Go to this address please and fill in the details"
        print api.get_authorize_url()
        print "----------------"
        
        result = []
        httpd = self._create_http_server(result)
        httpd.handle_request()
        httpd.server_close()
        
        api._verifier = result[0]
        api.access_token()

if __name__ == "__main__":
    unittest.main()