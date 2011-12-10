from linkedin.tests import *
from linkedin import linkedin
from random import randint

class LinkedInMethodsTestBase:
    
    @classmethod
    def set_up_class(cls, gae):
        cls._gae = gae
        cls.api = linkedin.LinkedIn(API_KEY, SECRET_KEY, RETURN_URL, gae)
        cls.request_token_ret_val = cls.api.request_token()

        if (cls.request_token_ret_val):        
            print "----------------"
            print "Go to this address please and fill in the details"
            print cls.api.get_authorize_url()
            print "----------------"
            
            cls._create_http_server(cls.api)
            cls.httpd.handle_request()
            cls.httpd.server_close()
            cls.api.access_token()
    
    def _generate_email(self):
        return "mail_for_tests" + str(randint(1, 1000)) + "@nothing.com"
    
    def test_get_profile(self):
        self.assertTrue(self.api.get_profile(fields=['first-name', 'last-name']), self.api.get_error())
    
    def test_get_connections(self):
        self.assertTrue(self.api.get_connections(), self.api.get_error())
        
    def test_get_search(self):
        self.assertTrue(self.api.get_search({"name" : "Iftach Bar"}), self.api.get_error())
        self.assertTrue(self.api.get_search({}), self.api.get_error())
        
    def test_send_message(self):
        self.assertTrue(self.api.send_message("python linkedin integration test",
                    "This is the message. GAE : " + str(self._gae),
                    send_yourself = True), self.api.get_error())
        
    def test_send_invitation(self):
        self.assertTrue(self.api.send_invitation("python linkedin integration test",
                    "This is the message. GAE : " + str(self._gae),
                    "first",
                    "last",
                    self._generate_email()), self.api.get_error())
        
    def test_set_and_clear_status(self):
        self.assertTrue(self.api.set_status("Testing linkedin API"),
                        self.api.get_error())
        self.assertTrue(self.api.clear_status(), self.api.get_error())
        
    def test_share_comment(self):
        self.assertTrue(self.api.share_update(comment = "Testing linkedin API"),
                        self.api.get_error())
        self.assertTrue(self.api.clear_status(), self.api.get_error())

class LinkedInRegularTest(LinkedInMethodsTestBase, LinkedInTestBase):
    
    @classmethod
    def setUpClass(cls):
        cls.set_up_class(False)

