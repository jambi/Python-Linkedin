from linkedin.tests import *
from linkedin.new_api import *

from nose.tools import raises

class NewApiRequestTest(LinkedInTestBase):
    
    def test_access_token_no_error(self):
        api = LinkedIn2().api_key(API_KEY).secret_key(SECRET_KEY) \
        .callback_url(RETURN_URL).request_token()

        url = api.get_authorize_url()
        verifier = self._wait_for_user_to_get_verifier(url)
        
        api.verifier(verifier).access_token()
    
    def test_access_token_gae_no_error(self):
        self._init_gae()
        api = LinkedIn2().api_key(API_KEY).secret_key(SECRET_KEY) \
        .callback_url(RETURN_URL).gae().request_token()
        
        url = api.get_authorize_url()
        verifier = self._wait_for_user_to_get_verifier(url)
        
        api.verifier(verifier).access_token()
        
    @raises(ConfigurationError)
    def test_access_token_before_basic_configuration(self):
        LinkedIn2().access_token()
        
    @raises(ConfigurationError)
    def test_access_token_before_basic_configuration2(self):
        LinkedIn2().api_key(API_KEY).access_token()
        
    @raises(ConfigurationError)
    def test_access_token_before_basic_configuration3(self):
        LinkedIn2().secret_key(API_KEY).access_token()
        
    @raises(ConfigurationError)
    def test_access_token_before_basic_configuration4(self):
        LinkedIn2().secret_key(SECRET_KEY).api_key(API_KEY).access_token()
        
    @raises(ConfigurationError)
    def test_access_token_before_basic_configuration5(self):
        LinkedIn2().callback_url(RETURN_URL).api_key(API_KEY).access_token()
    
    @raises(ConfigurationError)
    def test_access_token_before_basic_configuration6(self):
        LinkedIn2().callback_url(RETURN_URL).secret_key(SECRET_KEY).access_token()
    
    @raises(ConfigurationError)
    def test_access_token_before_basic_configuration7(self):
        LinkedIn2().callback_url(RETURN_URL).access_token()
    
    @raises(ConfigurationError)
    def test_access_token_before_request_token(self):
        LinkedIn2().api_key(API_KEY).secret_key(SECRET_KEY) \
        .callback_url(RETURN_URL).access_token()
        
    @raises(ConfigurationError)
    def test_access_token_before_verifier(self):
        LinkedIn2().api_key(API_KEY).secret_key(SECRET_KEY) \
        .callback_url(RETURN_URL).request_token().access_token()
    
    @raises(ConfigurationError)
    def test_access_token_twice(self):
        LinkedIn2().api_key(API_KEY).secret_key(SECRET_KEY) \
        .callback_url(RETURN_URL).access_token().access_token()
        
    @raises(ConfigurationError)
    def test_get_authorize_url_before_request_token(self):
        LinkedIn2().api_key(API_KEY).secret_key(SECRET_KEY) \
        .callback_url(RETURN_URL).get_authorize_url()
        
    def test_reset(self):
        api = LinkedIn2()
        for i in range(2):
            api.api_key(API_KEY).secret_key(SECRET_KEY) \
            .callback_url(RETURN_URL).request_token()
            
            url = api.get_authorize_url()
            verifier = self._wait_for_user_to_get_verifier(url)
            
            api.verifier(verifier).access_token()
            api.reset()
        
    def _wait_for_user_to_get_verifier(self, url):
        print "----------------"
        print "Go to this address please and fill in the details"
        print url
        print "----------------"
        
        result = []
        httpd = self._create_http_server(result)
        httpd.handle_request()
        httpd.server_close()
        return result[0]
        