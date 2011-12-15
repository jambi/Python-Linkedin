from tests import *
from linkedin import linkedin
from random import randint

class LinkedInMethodsTestBase:
    
    @classmethod
    def set_up_class(cls, gae):
        cls._gae = gae
        cls.api = linkedin.LinkedIn(API_KEY, SECRET_KEY, RETURN_URL, gae)
        cls.api.request_token()

        print "----------------"
        print "Go to this address please and fill in the details"
        print cls.api.get_authorize_url()
        print "----------------"
        
        result = []
        httpd = cls._create_http_server(result)
        httpd.handle_request()
        httpd.server_close()
        cls.api._verifier = result[0]
        cls.api.access_token()
    
    def _generate_email(self):
        return "mail_for_tests" + str(randint(1, 1000)) + "@nothing.com"
    
    def test_get_profile(self):
        self.assertTrue(self.api.get_profile(fields=['first-name', 'last-name']))
        
    def test_default_get_profile(self):
        p = self.api.get_profile()
        self.assertTrue(p)
        self.assertTrue(p.first_name)
        self.assertTrue(p.last_name)
        self.assertTrue(p.headline)
        self.assertTrue(p.private_url)
    
    def test_get_connections(self):
        self.assertTrue(self.api.get_connections())
        
    def test_get_search(self):
        self.assertTrue(self.api.get_search({"name" : "Iftach Bar"}))
        self.assertTrue(self.api.get_search({}))
        
    def test_send_message(self):
        "send_message doesn't raise error"
        self.api.send_message("python linkedin integration test",
                    "This is the message. GAE : " + str(self._gae),
                    send_yourself = True)
        
    def test_send_invitation(self):
        "send_invitation doesn't raise error"
        self.api.send_invitation("python linkedin integration test",
                    "This is the message. GAE : " + str(self._gae),
                    "first",
                    "last",
                    self._generate_email())
        
    def test_set_and_clear_status(self):
        "set_status and clear_status don't raise error"
        self.api.set_status("Testing linkedin API")
        self.api.clear_status()
        
    def test_share_comment(self):
        "share_update and clear_status don't raise error"
        self.api.share_update(comment = "Testing linkedin API")
        self.api.clear_status()

class LinkedInRegularTest(LinkedInMethodsTestBase, LinkedInTestBase):
    
    @classmethod
    def setUpClass(cls):
        cls.set_up_class(False)

