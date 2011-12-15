from linkedin import LinkedIn

class ConfigurationError(Exception):
    def __init__(self, error):
        self._error = error
        
    def __str__(self):
        return repr(self._error)

from functools import partial

class Fields(object):
    
    def _init_values(self, simple_fields, complex_fields=None):
        if complex_fields is None: complex_fields = {} 
        self._values = dict()
         
        for key in simple_fields:
            self._values[key] = False
            method_key = "add_" + key.replace("-", "_")
            function = partial(self._set_field, key)
            # TODO initialize the name of the function
            self.__dict__[method_key] = function
            
        for key, class_type in complex_fields.items():
            self._values[key] = False
            method_key = "add_" + key.replace("-", "_")
            function = partial(self._set_complex_field, key, class_type)
            # TODO initialize the name of the function
            self.__dict__[method_key] = function
    
    def __repr__(self):
        rep = []
        for key, value in self._values.items():
            if value is True:
                rep.append(key)
            elif isinstance(value, Fields):
                rep.append("{key}:({value})".format(key=key, value=repr(value)))
            elif value:
                rep.append(value)
        return self.__class__.__name__ + " : " + repr(rep)
            
    def _set_field(self, key):
        self._check_key_valid(key)
        
        self._values[key] = True
        return self
    
    def _check_key_valid(self, key):
        if not self._values.has_key(key):
            raise ValueError("{0} is not a valid field".format(key))
        
    def _set_complex_field(self, key, class_type, value=None):
        if not value:
            return self._set_field(key)
        
        self._check_key_valid(key)
        
        if not isinstance(value, class_type):
            raise ValueError("{0} is not of type {1}".format(value, class_type))
        
        self._values[key] = value
        return self
    
    def get_url(self):
        url_values = [key for key in self._values.keys() if self._values[key] is True]
        for key, value in self._values.items():
            if isinstance(value, Fields):
                url_values.append("{key}:({value})".format(key=key, value=value.get_url()))
            elif not isinstance(value, bool):
                url_values.append(value)
                
        return ",".join(url_values)

class Location(Fields):

    def __init__(self):
        self._init_values(("name",))
        
    def add_country_code(self):
        self._values["country-code"] = "country:(code)"
        return self
    
class RelationToViewer(Fields):
    def __init__(self):
        self._init_values(("distance", "num-related-connections", "related-connections"))
        
class MemberUrl(Fields):
    def __init__(self):
        self._init_values(("url", "name"))
        
class HttpHeader(Fields):
    def __init__(self):
        self._init_values(("name", "value"))
        
class HttpRequest(Fields):
    def __init__(self):
        self._init_values(("url",), {"headers" : HttpHeader})

class Profile(Fields):
    # Dont forget about these params: https://developer.linkedin.com/thread/2286
    def __init__(self):
        simple_fields = ("id",
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
            "public-profile-url",
            "site-standard-profile-request",
            "api-public-profile-request",
            "site-public-profile-request",
            )
        complex_fields = {
            "location" : Location,
            "relation-to-viewer" : RelationToViewer,
            "member-url-resources" : MemberUrl,
            "api-standard-profile-request" : HttpRequest}
        
        self._init_values(simple_fields, complex_fields)
        
        self._id = None
        self._url = None
        self._public = False
    
    def me(self):
        self._id = None
        self._url = None
        return self
        
    def set_url(self, url):
        self._id = None
        self._url = url
        return self
        
    def set_id(self, _id):
        self._url = None
        self._id = _id
        return self
    
    def public(self):
        self._public = True
        return self
    
    def private(self):
        self._public = False
        return self
        
    def get_url_for_api(self):
        url = ""
        if self._id:
            url = "id={0}".format(self._id)
        elif self._url:
            url = "url={0}".format(self._url)
        else:
            url = "~"
            
        if self._public:
            url += ":public"
        
        fields = self.get_url()
        if fields:
            url += ":(" + fields + ")"
        
        return url
    
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
        
    def profile(self, params):
        # TODO should we check if this is instance of ProfileParams?
        return self._linkedin.get_profile_raw(params.get_url_for_api())
    