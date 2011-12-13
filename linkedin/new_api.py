from linkedin import LinkedIn

class ConfigurationError(Exception):
    def __init__(self, error):
        self._error = error
        
    def __str__(self):
        return repr(self._error)

class ProfileFields(object):
    possible_fields = ("id",
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
        "main_address",
        "member-url-resources",
        "picture-url",
        "public-profile-url")
    
    def __init__(self):
        self.values = dict()
         
        for key in self.possible_fields:
#            self.__dict__[key.replace("-", "_")] = False
            key = key.replace("-", "_")
            self.values[key] = False
#            setattr(self, key, None)
            
    def __getattr__(self, name):
        return lambda: self._set_field(name)
    
    def _set_field(self, key):
        print "key ", key
        self.values[key] = True

class ProfileAction(object):
    def __init__(self, linkedin):
        self._linkedin = linkedin
        
        self._url = None
        self._id = None
        self._fields = {}
        
    def id(self, id):
        if self._url:
            # Bad state, only url or id, raise error
            raise Exception
        
        self._id = id
        return self
    
    def url(self, url):
        if self._id:
            # Bad state, only url or id, raise error
            raise Exception
        
        self._url = url
        return self
        
    def fields(self, fields):
        return self
    
    def allfields(self):
        return self
    
    def field(self, name, val):
        self._fields[name] = val
        return self
    
    def raw(self, raw):
        return self._linkedin.get_profile_raw(raw)
    
    def fetch(self):
        return self._linkedin.get_profile(self._id, self._url, self._fields)

class LinkedIn2(object):
    
    def __init__(self):
        self._linkedin = LinkedIn(None, None, None, False)
    
    def api_key(self, api_key):
        self._linkedin._api_key = api_key
        return self
        
    def secret_key(self, api_secret):
        self._linkedin._api_secret = api_secret
        return self
        
    def callback_url(self, callback_url):
        self._linkedin._callback_url = callback_url
        return self
    
    def gae(self):
        self._linkedin._gae = True
        return self
        
    def nogae(self):
        self._linkedin._gae = False
        return self
        
    def reset(self):
        self._linkedin.clear()
        return self
    

    def _check_basic_parameters(self):
        if not self._linkedin._api_key:
            raise ConfigurationError("Please run api_key() first")
        if not self._linkedin._api_secret:
            raise ConfigurationError("Please run secret_key() first")
        if not self._linkedin._callback_url:
            raise ConfigurationError("Please run callback_url() first")

    def request_token(self):
        self._check_basic_parameters()
        
        if self._linkedin._request_token or self._linkedin._access_token or \
            self._linkedin._verifier or self._linkedin._request_token_secret or \
            self._linkedin._access_token_secret:
            raise ConfigurationError("Please run reset() before running request_token again")
        
        self._linkedin.request_token()
        return self
    
    def get_authorize_url(self):
        if not (self._linkedin._request_token):
            raise ConfigurationError("Please run request_token() before running get_authorize_url()")
        return self._linkedin.get_authorize_url()
        
    def verifier(self, verifier):
        self._linkedin._verifier = verifier
        return self
    
    def access_token(self):
        if not (self._linkedin._request_token and self._linkedin._request_token_secret):
            raise ConfigurationError("Please run request_token() before running access_token()")
        
        if not self._linkedin._verifier:
            raise ConfigurationError("Please run verifier() before running access_token()")
        
        if self._linkedin._access_token or self._linkedin._access_token_secret:
            raise ConfigurationError("Please run reset() before running access_token again")
        
        self._linkedin.access_token()
        return self
        
    def profile(self):
        return ProfileAction(self._linkedin)
    