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
        helper.quick_api(API_KEY, SECRET_KEY)

if __name__ == "__main__":
    unittest.main()