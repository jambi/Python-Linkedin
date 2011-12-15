from tests import *
from linkedin.api import *

from nose.tools import raises

class NewApiRequestTest(LinkedInTestBase):
    
    def test_request_token_no_error(self):
        LinkedIn().api_key(API_KEY).secret_key(SECRET_KEY) \
        .callback_url(RETURN_URL).request_token()
    
    def test_request_token_gae_no_error(self):
        self._init_gae()
        LinkedIn().api_key(API_KEY).secret_key(SECRET_KEY) \
        .callback_url(RETURN_URL).gae().request_token()
        
    @raises(ConfigurationError)
    def test_request_token_before_basic_configuration(self):
        LinkedIn().request_token()
        
    @raises(ConfigurationError)
    def test_request_token_before_basic_configuration2(self):
        LinkedIn().api_key(API_KEY).request_token()
        
    @raises(ConfigurationError)
    def test_request_token_before_basic_configuration3(self):
        LinkedIn().secret_key(API_KEY).request_token()
        
    @raises(ConfigurationError)
    def test_request_token_before_basic_configuration4(self):
        LinkedIn().secret_key(SECRET_KEY).api_key(API_KEY).request_token()
        
    @raises(ConfigurationError)
    def test_request_token_before_basic_configuration5(self):
        LinkedIn().callback_url(RETURN_URL).api_key(API_KEY).request_token()
    
    @raises(ConfigurationError)
    def test_request_token_before_basic_configuration6(self):
        LinkedIn().callback_url(RETURN_URL).secret_key(SECRET_KEY).request_token()
    
    @raises(ConfigurationError)
    def test_request_token_before_basic_configuration7(self):
        LinkedIn().callback_url(RETURN_URL).request_token()
    
    @raises(ConfigurationError)
    def test_request_token_twice(self):
        LinkedIn().api_key(API_KEY).secret_key(SECRET_KEY) \
        .callback_url(RETURN_URL).request_token().request_token()
        
    def test_reset(self):
        LinkedIn().api_key(API_KEY).secret_key(SECRET_KEY) \
        .callback_url(RETURN_URL).request_token().reset().request_token()
        