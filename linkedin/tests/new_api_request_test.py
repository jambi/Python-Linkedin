from linkedin.tests import *
from linkedin.new_api import *

from nose.tools import raises

class NewApiRequestTest(LinkedInTestBase):
    
    def test_request_token_no_error(self):
        LinkedIn2().api_key(API_KEY).secret_key(SECRET_KEY) \
        .callback_url(RETURN_URL).request_token()
    
    def test_request_token_gae_no_error(self):
        self._init_gae()
        LinkedIn2().api_key(API_KEY).secret_key(SECRET_KEY) \
        .callback_url(RETURN_URL).gae().request_token()
        
    @raises(ConfigurationError)
    def test_request_token_before_basic_configuration(self):
        LinkedIn2().request_token()
        
    @raises(ConfigurationError)
    def test_request_token_before_basic_configuration2(self):
        LinkedIn2().api_key(API_KEY).request_token()
        
    @raises(ConfigurationError)
    def test_request_token_before_basic_configuration3(self):
        LinkedIn2().secret_key(API_KEY).request_token()
        
    @raises(ConfigurationError)
    def test_request_token_before_basic_configuration4(self):
        LinkedIn2().secret_key(SECRET_KEY).api_key(API_KEY).request_token()
        
    @raises(ConfigurationError)
    def test_request_token_before_basic_configuration5(self):
        LinkedIn2().callback_url(RETURN_URL).api_key(API_KEY).request_token()
    
    @raises(ConfigurationError)
    def test_request_token_before_basic_configuration6(self):
        LinkedIn2().callback_url(RETURN_URL).secret_key(SECRET_KEY).request_token()
    
    @raises(ConfigurationError)
    def test_request_token_before_basic_configuration7(self):
        LinkedIn2().callback_url(RETURN_URL).request_token()
    
    @raises(ConfigurationError)
    def test_request_token_twice(self):
        LinkedIn2().api_key(API_KEY).secret_key(SECRET_KEY) \
        .callback_url(RETURN_URL).request_token().request_token()
        
    def test_reset(self):
        LinkedIn2().api_key(API_KEY).secret_key(SECRET_KEY) \
        .callback_url(RETURN_URL).request_token().reset().request_token()
        