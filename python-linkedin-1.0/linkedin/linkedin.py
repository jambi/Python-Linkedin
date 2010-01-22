# -*- coding: utf-8 -*-

#######################################################################################
# Python implementation of LinkedIn OAuth Authorization, Profile and Connection APIs. #
#                                                                                     #
# Author: Ozgur Vatansever                                                            #
# Email : ozgurvt@gmail.com                                                           #
# LinkedIn Account: http://tr.linkedin.com/in/ozgurv                                  #
#######################################################################################


import urllib, urllib2, time, random, httplib, hmac, hashlib, binascii, cgi, string, datetime

from xml.dom import minidom
from urlparse import urlparse
from xml.sax.saxutils import unescape

class OAuthError(Exception):
    """
    General OAuth exception, nothing special.
    """
    def __init__(self, value):
        self.parameter = value
        
    def __str__(self):
        return repr(self.parameter)


class Education(object):
    """
    Class that wraps an education info of a user
    """
    def __init__(self):
        self.id          = None
        self.school_name = None
        self.degree      = None

    @staticmethod
    def create(node):
        """
        <educations total="">
         <education>
          <id>
          <school-name>
          <degree>
          <start-date>
           <year>
          </start-date>
          <end-date>
           <year>
          </end-date>
         </education>
        </educations>
        """
        children = node.getElementsByTagName("education")
        result = []
        for child in children:
            education = Education()
            education.id = education._get_child(child, "id")
            education.school_name = education._get_child(child, "school-name")
            education.degree = education._get_child(child, "degree")
            result.append(education)            
        return result
    
    def _get_child(self, node, tagName):
        try:
            domNode = node.getElementsByTagName(tagName)[0]
            childNodes = domNode.childNodes
            if childNodes:
                return childNodes[0].nodeValue
            return None
        except:
            return None

    
class Position(object):
    """
    Class that wraps a business position info of a user
    """
    def __init__(self):
        self.id         = None
        self.title      = None
        self.summary    = None
        self.start_date = None
        self.company    = None
        
    @staticmethod
    def create(node):
        """
        <positions total='1'>
         <position>
          <id>101526695</id>
          <title>Developer</title>
          <summary></summary>
          <start-date>
          <year>2009</year>
          <month>9</month>
          </start-date>
          <is-current>true</is-current>
          <company>
          <name>Akinon</name>
          </company>
         </position>
        </positions>
        """
        children = node.getElementsByTagName("position")
        result = []
        for child in children:
            position = Position()
            position.id = position._get_child(child, "id")
            position.title = position._get_child(child, "title")
            position.summary = position._get_child(child, "summary")
            company = child.getElementsByTagName("company")
            if company:
                company = company[0]
                position.company = position._get_child(company, "name")
            
            start_date = child.getElementsByTagName("start-date")
            if start_date:
                start_date = start_date[0]
                try:
                    year = int(position._get_child(start_date, "year"))
                    month = int(position._get_child(start_date, "month"))
                    position.start_date = datetime.date(year, month, 1)
                except Exception, detail:
                    pass
            result.append(position)

        return result
            

    def _get_child(self, node, tagName):
        try:
            domNode = node.getElementsByTagName(tagName)[0]
            childNodes = domNode.childNodes
            if childNodes:
                return childNodes[0].nodeValue
            return None
        except:
            return None
    
class Profile(object):
    """
    Wraps the data which comes from Profile API of LinkedIn.
    For further information, take a look at LinkedIn Profile API.
    """
    def __init__(self):
        self.id          = None
        self.first_name  = None
        self.last_name   = None
        self.location    = None
        self.industry    = None
        self.summary     = None
        self.specialties = None
        self.interests   = None
        self.honors      = None
        self.positions   = []
        self.educations  = []
        self.public_url  = None
        self.picture_url = None
        self.current_status = None
        
    @staticmethod
    def create(xml_string):
        """
        @This method is a static method so it shouldn't be called from an instance.
        
        Parses the given xml string and results in a Profile instance.
        If the given instance is not valid, this method returns NULL.
        """
        try:
            document = minidom.parseString(xml_string)
            person = document.getElementsByTagName("person")[0]
            profile = Profile()
            profile.id = profile._get_child(person, "id")
            profile.first_name = profile._get_child(person, "first-name")
            profile.last_name = profile._get_child(person, "last-name")
            profile.headline = profile._get_child(person, "headline")
            profile.specialties = profile._get_child(person, "specialties")
            profile.industry = profile._get_child(person, "industry")
            profile.honors = profile._get_child(person, "honors")
            profile.picture_url = profile._unescape(profile._get_child(person, "picture-url"))
            profile.current_status = profile._get_child(person, "current-status")

            # create location
            location = person.getElementsByTagName("location")
            if location:
                location = location[0]
                profile.location = profile._get_child(location, "name")

            # create public profile url
            public_profile = person.getElementsByTagName("site-public-profile-request")
            if public_profile:
                public_profile = public_profile[0]
                profile.public_url = profile. _get_child(public_profile, "url")

            # create positions
            positions = person.getElementsByTagName("positions")
            if positions:
                positions = positions[0]
                profile.positions = Position.create(positions)

            # create educations
            educations = person.getElementsByTagName("educations")
            if educations:
                educations = educations[0]
                profile.educations = Education.create(educations)

            return profile
        except:
            return None

        return None

    def _unescape(self, url):
        if url:
            return unescape(url)
        return url

    def _get_child(self, node, tagName):
        try:
            domNode = node.getElementsByTagName(tagName)[0]
            if domNode.parentNode.tagName == node.tagName:
                childNodes = domNode.childNodes
                if childNodes:
                    return childNodes[0].nodeValue
                return None
            else:
                return None
        except:
            return None

    
class LinkedIn(object):
    def __init__(self, api_key, api_secret, callback_url):
        """
        LinkedIn Base class that simply implements LinkedIn OAuth Authorization and LinkedIn APIs such as Profile, Connection vs.

        @ LinkedIn OAuth Authorization
        ------------------------------
        In OAuth terminology, there are 2 tokens that we need in order to have permission to perform an API request.
        Those are requestToken and accessToken. Thus, this class basicly intends to wrap methods of OAuth spec. which
        are related of gettting requestToken and accessToken strings.

        @ Important Note:
        -----------------
        HMAC-SHA1 hashing algorithm will be used while encrypting a request body of an HTTP request. Other alternatives
        such as 'SHA-1' or 'PLAINTEXT' are ignored.

        @Reference for OAuth
        --------------------
        Please take a look at the link below if you have a basic knowledge of HTTP protocol
        - http://developer.linkedin.com/docs/DOC-1008

        
        Please create an application from the link below if you do not have an API key and secret key yet.
        - https://www.linkedin.com/secure/developer
        @api_key:    Your API key
        @api_secret: Your API secret key
        @callback_url: the return url when the user grants permission to Consumer.
        """
        # Credientials
        self.URI_SCHEME        = "https"
        self.API_ENDPOINT      = "api.linkedin.com"
        self.REQUEST_TOKEN_URL = "/uas/oauth/requestToken"
        self.ACCESS_TOKEN_URL  = "/uas/oauth/accessToken"
        self.REDIRECT_URL      = "/uas/oauth/authorize"
        self.version           = "1.0"
        self.signature_method  = "HMAC-SHA1" # as I said
        self.BASE_URL          = "%s://%s" % (self.URI_SCHEME, self.API_ENDPOINT)
        
        self.API_KEY       = api_key
        self.API_SECRET    = api_secret
        self.CALLBACK_URL  = callback_url
        self.request_token = None # that comes later
        self.access_token  = None # that comes later and later
        
        self.request_token_secret = None
        self.access_token_secret  = None
        
        self.verifier = None
        self.error    = None

        self.request_oauth_nonce     = None
        self.request_oauth_timestamp = None
        self.access_oauth_nonce      = None
        self.access_oauth_timestamp  = None
        self.request_oauth_error     = None
        self.access_oauth_error      = None
        

    def getRequestTokenURL(self):
        return "%s://%s%s" % (self.URI_SCHEME, self.API_ENDPOINT, self.REQUEST_TOKEN_URL)

    def getAccessTokenURL(self):
        return "%s://%s%s" % (self.URI_SCHEME, self.API_ENDPOINT, self.ACCESS_TOKEN_URL)

    def getAuthorizeURL(self, request_token = None):
        self.request_token = request_token if request_token is not None else self.request_token
        if self.request_token is None:
            raise OAuthError("OAuth Request Token is NULL. Plase acquire this first.")
        return "%s%s?oauth_token=%s" % (self.BASE_URL, self.REDIRECT_URL, self.request_token) 
    
    #################################################
    # HELPER FUNCTIONS                              #
    # You do not explicitly use those methods below #
    #################################################
    def _generate_nonce(self, length = 20):
        return ''.join([string.letters[random.randint(0, len(string.letters) - 1)] for i in range(length)])

    def _generate_timestamp(self):
        return int(time.time())
    
    def _quote(self, st):
        return urllib.quote(st, safe='~')

    def _utf8(self, st):
        return st.encode("utf-8") if isinstance(st, unicode) else str(st)

    def _urlencode(self, query_dict):
        keys_and_values = [(self._quote(self._utf8(k)), self._quote(self._utf8(v))) for k,v in query_dict.items()]
        keys_and_values.sort()
        return '&'.join(['%s=%s' % (k, v) for k, v in keys_and_values])

    def _get_value_from_raw_qs(self, key, qs):
        raw_qs = cgi.parse_qs(qs, keep_blank_values = False)
        rs = raw_qs.get(key)
        if type(rs) == list:
            return rs[0]
        else:
            return rs

    def _signature_base_string(self, method, uri, query_dict):
        return "&".join([self._quote(method), self._quote(uri), self._quote(self._urlencode(query_dict))])
        
    def _parse_error(self, str_as_xml):
        """
        Helper function in order to get error message from an xml string.
        In coming xml can be like this:
        <?xml version='1.0' encoding='UTF-8' standalone='yes'?>
        <error>
         <status>404</status>
         <timestamp>1262186271064</timestamp>
         <error-code>0000</error-code>
         <message>[invalid.property.name]. Couldn't find property with name: first_name</message>
        </error>
        """
        try:
            xmlDocument = minidom.parseString(str_as_xml)
            if len(xmlDocument.getElementsByTagName("error")) > 0: 
                error = xmlDocument.getElementsByTagName("message")
                if error:
                    error = error[0]
                    return error.childNodes[0].nodeValue
            return None
        except Exception, detail:
            raise OAuthError("Invalid XML String given: error: %s" % repr(detail))
        
    ########################
    # END HELPER FUNCTIONS #
    ########################

    def requestToken(self):
        """
        Performs the corresponding API which returns the request token in a query string
        The POST Querydict must include the following:
         * oauth_callback
         * oauth_consumer_key
         * oauth_nonce
         * oauth_signature_method
         * oauth_timestamp
         * oauth_version
        """
        #################
        # BEGIN ROUTINE #
        #################
        # clear everything
        self.clear()
        # initialization
        self.request_oauth_nonce = self._generate_nonce()
        self.request_oauth_timestamp = self._generate_timestamp()
        # create Signature Base String
        method = "POST"
        url = self.getRequestTokenURL()
        query_dict = {"oauth_callback": self.CALLBACK_URL,
                      "oauth_consumer_key": self.API_KEY,
                      "oauth_nonce": self.request_oauth_nonce,
                      "oauth_signature_method": self.signature_method,
                      "oauth_timestamp": self.request_oauth_timestamp,
                      "oauth_version": self.version,
                      }
        query_string = self._quote(self._urlencode(query_dict))
        signature_base_string = "&".join([self._quote(method), self._quote(url), query_string])
        # create actual signature
        hashed = hmac.new(self._quote(self.API_SECRET) + "&", signature_base_string, hashlib.sha1)
        signature = binascii.b2a_base64(hashed.digest())[:-1]
        # it is time to create the heaader of the http request that will be sent
        header = 'OAuth realm="http://api.linkedin.com", '
        header += 'oauth_nonce="%s", '
        header += 'oauth_callback="%s", '
        header += 'oauth_signature_method="%s", '
        header += 'oauth_timestamp="%d", '
        header += 'oauth_consumer_key="%s", '
        header += 'oauth_signature="%s", '
        header += 'oauth_version="%s"'
        header = header % (self.request_oauth_nonce, self._quote(self.CALLBACK_URL),
                           self.signature_method, self.request_oauth_timestamp,
                           self._quote(self.API_KEY), self._quote(signature), self.version)

        
        # next step is to establish an HTTPS connection through the LinkedIn API
        # and fetch the request token.
        connection = httplib.HTTPSConnection(self.API_ENDPOINT)
        connection.request(method, self.REQUEST_TOKEN_URL, body = self._urlencode(query_dict), headers = {'Authorization': header})
        response = connection.getresponse()
        if response is None:
            self.request_oauth_error = "No HTTP response received."
            connection.close()
            return False

        response = response.read()
        connection.close()
        
        oauth_problem = self._get_value_from_raw_qs("oauth_problem", response)
        if oauth_problem:
            self.request_oauth_error = oauth_problem
            return False

        self.request_token = self._get_value_from_raw_qs("oauth_token", response)
        self.request_token_secret = self._get_value_from_raw_qs("oauth_token_secret", response)
        return True


    def accessToken(self, request_token = None, request_token_secret = None, verifier = None):
        """
        Performs the corresponding API which returns the access token in a query string
        Accroding to the link (http://developer.linkedin.com/docs/DOC-1008), POST Querydict must include the following:
        * oauth_consumer_key
        * oauth_nonce
        * oauth_signature_method
        * oauth_timestamp
        * oauth_token (request token)
        * oauth_version
        """
        #################
        # BEGIN ROUTINE #
        #################
        self.request_token = request_token if request_token is not None else self.request_token
        self.request_token_secret = request_token_secret is not None if request_token_secret else self.request_token_secret
        self.verifier = verifier if verifier is not None else self.verifier
        # if there is no request token, fail immediately
        if self.request_token is None:
            raise OAuthError("There is no Request Token. Please perform 'requestToken' method and obtain that token first.")

        if self.request_token_secret is None:
            raise OAuthError("There is no Request Token Secret. Please perform 'requestToken' method and obtain that token first.")

        if self.verifier is None:
            raise OAuthError("There is no Verifier Key. Please perform 'requestToken' method, redirect user to API authorize page and get the verifier.")
        
        # initialization
        self.access_oauth_nonce = self._generate_nonce()
        self.access_oauth_timestamp = self._generate_timestamp()

        # create Signature Base String
        method = "POST"
        url = self.getAccessTokenURL()
        query_dict = {"oauth_consumer_key": self.API_KEY,
                      "oauth_nonce": self.access_oauth_nonce,
                      "oauth_signature_method": self.signature_method,
                      "oauth_timestamp": self.access_oauth_timestamp,
                      "oauth_token" : self.request_token,
                      "oauth_verifier" : self.verifier,
                      "oauth_version": self.version,
                      }
        query_string = self._quote(self._urlencode(query_dict))
        signature_base_string = "&".join([self._quote(method), self._quote(url), query_string])
        # create actual signature
        hashed = hmac.new(self._quote(self.API_SECRET) + "&" + self._quote(self.request_token_secret), signature_base_string, hashlib.sha1)
        signature = binascii.b2a_base64(hashed.digest())[:-1]
        # it is time to create the heaader of the http request that will be sent
        header = 'OAuth realm="http://api.linkedin.com", '
        header += 'oauth_nonce="%s", '
        header += 'oauth_signature_method="%s", '
        header += 'oauth_timestamp="%d", '
        header += 'oauth_consumer_key="%s", '
        header += 'oauth_token="%s", '
        header += 'oauth_verifier="%s", '
        header += 'oauth_signature="%s", '
        header += 'oauth_version="%s"'
        header = header % (self._quote(self.access_oauth_nonce), self._quote(self.signature_method),
                           self.access_oauth_timestamp, self._quote(self.API_KEY),
                           self._quote(self.request_token), self._quote(self.verifier),
                           self._quote(signature), self._quote(self.version))

        # next step is to establish an HTTPS connection through the LinkedIn API
        # and fetch the request token.
        connection = httplib.HTTPSConnection(self.API_ENDPOINT)
        connection.request(method, self.ACCESS_TOKEN_URL, body = self._urlencode(query_dict), headers = {'Authorization': header})
        response = connection.getresponse()
        if response is None:
            self.request_oauth_error = "No HTTP response received."
            connection.close()
            return False

        response = response.read()
        connection.close()
        oauth_problem = self._get_value_from_raw_qs("oauth_problem", response)
        if oauth_problem:
            self.request_oauth_error = oauth_problem
            return False

        self.access_token = self._get_value_from_raw_qs("oauth_token", response)
        self.access_token_secret = self._get_value_from_raw_qs("oauth_token_secret", response)
        return True


    def GetProfile(self, member_id = None, url = None, *fields):
        """
        Gets the public profile for a specific user. It is determined by his/her member id or public url.
        If none of them is given, the information og the application's owner are returned.

        If none of them are given, current user's details are fetched.
        The argument '*fields' determines howmuch information will be fethced.

        Examples:
        client.GetProfile(merber_id = 123, url = None, 'first-name', 'last-name') : fetches the profile of a user whose id is 123. 

        client.GetProfile(merber_id = None, url = None, 'first-name', 'last-name') : fetches current user's profile

        client.GetProfile(member_id = None, 'http://www.linkedin.com/in/ozgurv') : fetches the profile of a  user whose profile url is http://www.linkedin.com/in/ozgurv
        
        @ Returns Profile instance
        """
        #################
        # BEGIN ROUTINE #
        #################
        # if there is no access token or secret, fail immediately
        if self.access_token is None:
            self.error = "There is no Access Token. Please perform 'accessToken' method and obtain that token first."
            raise OAuthError(self.error)
        
        if self.access_token_secret is None:
            self.error = "There is no Access Token Secret. Please perform 'accessToken' method and obtain that token first."
            raise OAuthError(self.error)
        
        # specify the url according to the parameters given
        raw_url = "/v1/people/"
        if url:
            url = self._quote(url)
            raw_url = (raw_url + "url=%s:public") % url
        elif member_id:
            raw_url = (raw_url + "id=%s" % member_id)
        else:
            raw_url = raw_url + "~"
        if url is None:
            fields = ":(%s)" % ",".join(fields) if len(fields) > 0 else None
            if fields:
                raw_url = raw_url + fields
                
        # generate nonce and timestamp
        nonce = self._generate_nonce()
        timestamp = self._generate_timestamp()

        # create signatrue and signature base string
        method = "GET"
        FULL_URL = "%s://%s%s" % (self.URI_SCHEME, self.API_ENDPOINT, raw_url)
        query_dict = {"oauth_consumer_key": self.API_KEY,
                      "oauth_nonce": nonce,
                      "oauth_signature_method": self.signature_method,
                      "oauth_timestamp": timestamp,
                      "oauth_token" : self.access_token,
                      "oauth_version": self.version
                      }
        
        signature_base_string = "&".join([self._quote(method), self._quote(FULL_URL), self._quote(self._urlencode(query_dict))])
        hashed = hmac.new(self._quote(self.API_SECRET) + "&" + self._quote(self.access_token_secret), signature_base_string, hashlib.sha1)
        signature = binascii.b2a_base64(hashed.digest())[:-1]


        # create the HTTP header
        header = 'OAuth realm="http://api.linkedin.com", '
        header += 'oauth_nonce="%s", '
        header += 'oauth_signature_method="%s", '
        header += 'oauth_timestamp="%d", '
        header += 'oauth_consumer_key="%s", '
        header += 'oauth_token="%s", '
        header += 'oauth_signature="%s", '
        header += 'oauth_version="%s"'
        header = header % (nonce, self.signature_method, timestamp,
                           self._quote(self.API_KEY), self._quote(self.access_token),
                           self._quote(signature), self.version)
        

        # make the HTTP request
        connection = httplib.HTTPSConnection(self.API_ENDPOINT)
        connection.request(method, raw_url, headers = {'Authorization': header})
        response = connection.getresponse()

        # according to the response, decide what you want to do
        if response is None:
            self.error = "No HTTP response received."
            connection.close()
            return None

        response = response.read()
        connection.close()
        error = self._parse_error(response)
        if error:
            self.error = error
            return None

        return Profile.create(response) # this creates Profile instance or gives you null

    def GetConnections(self, member_id = None, public_url = None):
        """
        Fetches the connections of a user whose id is the given member_id or url is the given public_url
        If none of the parameters given, the connections of the current user are fetched.
        @Returns: a list of Profile instances or an empty list if there is no connection.

        Example urls:
        * http://api.linkedin.com/v1/people/~/connections (for current user)
        * http://api.linkedin.com/v1/people/id=12345/connections (fetch with member_id)
        * http://api.linkedin.com/v1/people/url=http%3A%2F%2Fwww.linkedin.com%2Fin%2Flbeebe/connections (fetch with public_url)
        """
        # check the requirements
        if (not self.access_token) or (not self.access_token_secret):
            self.error = "You do not have an access token. Plase perform 'accessToken()' method first."
            raise OAuthError(self.error)
        
        #################
        # BEGIN ROUTINE #
        #################
        
        # first we need to specify the url according to the parameters given
        raw_url = "/v1/people/%s/connections"
        if member_id:
            raw_url = raw_url % ("id=" + member_id)
        elif public_url:
            raw_url = raw_url % ("url=" + self._quote(public_url))
        else:
            raw_url = raw_url % "~"

        # generate nonce and timestamp
        nonce = self._generate_nonce()
        timestamp = self._generate_timestamp()
        
        # create signature and signature base string
        FULL_URL = "%s://%s%s" % (self.URI_SCHEME, self.API_ENDPOINT, raw_url)
        method = "GET"
        query_dict = {"oauth_consumer_key": self.API_KEY,
                      "oauth_nonce": nonce,
                      "oauth_signature_method": self.signature_method,
                      "oauth_timestamp": timestamp,
                      "oauth_token" : self.access_token,
                      "oauth_version": self.version
                      }
        
        signature_base_string = "&".join([self._quote(method), self._quote(FULL_URL), self._quote(self._urlencode(query_dict))])
        hashed = hmac.new(self._quote(self.API_SECRET) + "&" + self._quote(self.access_token_secret), signature_base_string, hashlib.sha1)
        signature = binascii.b2a_base64(hashed.digest())[:-1]

        # create the HTTP header
        header = 'OAuth realm="http://api.linkedin.com", '
        header += 'oauth_nonce="%s", '
        header += 'oauth_signature_method="%s", '
        header += 'oauth_timestamp="%d", '
        header += 'oauth_consumer_key="%s", '
        header += 'oauth_token="%s", '
        header += 'oauth_signature="%s", '
        header += 'oauth_version="%s"'
        header = header % (nonce, self.signature_method, timestamp,
                           self._quote(self.API_KEY), self._quote(self.access_token),
                           self._quote(signature), self.version)
        
        # make the request
        connection = httplib.HTTPSConnection(self.API_ENDPOINT)
        connection.request(method, raw_url, headers = {'Authorization': header})
        response = connection.getresponse()

        # according to the response, decide what you want to do
        if response is None:
            self.error = "No HTTP response received."
            connection.close()
            return None

        response = response.read()
        connection.close()
        error = self._parse_error(response)
        if error:
            self.error = error
            return None


        document = minidom.parseString(response)
        connections = document.getElementsByTagName("person")
        result = []
        for connection in connections:
            profile = Profile.create(connection.toxml())
            if profile is not None:
                result.append(profile)
        return result

    def GetSearch(self, parameters):
        """
        Use the Search API to find LinkedIn profiles using keywords,
        company, name, or other methods. This returns search results,
        which are an array of matching member profiles. Each matching
        profile is similar to a mini-profile popup view of LinkedIn
        member profiles.

        Request URL Structure:
        http://api.linkedin.com/v1/people?keywords=['+' delimited keywords]&name=[first name + last name]&company=[company name]&current-company=[true|false]&title=[title]&current-title=[true|false]&industry-code=[industry code]&search-location-type=[I,Y]&country-code=[country code]&postal-code=[postal code]&network=[in|out]&start=[number]&count=[1-10]&sort-criteria=[ctx|endorsers|distance|relevance]
        """
        # check the requirements
        if (not self.access_token) or (not self.access_token_secret):
            self.error = "You do not have an access token. Plase perform 'accessToken()' method first."
            raise OAuthError(self.error)

        # first we need to specify the url according to the parameters given
        raw_url = "/v1/people"
        request_url = "%s?%s" % (raw_url, self._urlencode(parameters))
        
        # generate nonce and timestamp
        nonce = self._generate_nonce()
        timestamp = self._generate_timestamp()
        
        # create signature and signature base string
        FULL_URL = "%s://%s%s" % (self.URI_SCHEME, self.API_ENDPOINT, raw_url)
        
        method = "GET"
        query_dict = {"oauth_consumer_key": self.API_KEY,
                      "oauth_nonce": nonce,
                      "oauth_signature_method": self.signature_method,
                      "oauth_timestamp": timestamp,
                      "oauth_token" : self.access_token,
                      "oauth_version": self.version
                      }
        query_dict.update(parameters)
        
        signature_base_string = "&".join([self._quote(method), self._quote(FULL_URL), self._quote(self._urlencode(query_dict))])
        hashed = hmac.new(self._quote(self.API_SECRET) + "&" + self._quote(self.access_token_secret), signature_base_string, hashlib.sha1)
        signature = binascii.b2a_base64(hashed.digest())[:-1]

        # create the HTTP header
        header = 'OAuth realm="http://api.linkedin.com", '
        header += 'oauth_nonce="%s", '
        header += 'oauth_signature_method="%s", '
        header += 'oauth_timestamp="%d", '
        header += 'oauth_consumer_key="%s", '
        header += 'oauth_token="%s", '
        header += 'oauth_signature="%s", '
        header += 'oauth_version="%s"'
        header = header % (nonce, self.signature_method, timestamp,
                           self._quote(self.API_KEY), self._quote(self.access_token),
                           self._quote(signature), self.version)

        # make the request
        connection = httplib.HTTPSConnection(self.API_ENDPOINT)
        connection.request(method, request_url, headers = {'Authorization': header})
        response = connection.getresponse()
        
        # according to the response, decide what you want to do
        if response is None:
            self.error = "No HTTP response received."
            connection.close()
            return None

        response = response.read()

        connection.close()
        error = self._parse_error(response)
        if error:
            self.error = error
            return None

        document = minidom.parseString(response)
        connections = document.getElementsByTagName("person")
        result = []
        for connection in connections:
            profile = Profile.create(connection.toxml())
            if profile is not None:
                result.append(profile)
        print result
        return result


    def getRequestTokenError(self):
        return self.request_oauth_error

    def getAccessTokenError(self):
        return self.access_oauth_error
    
    def getError(self):
        return self.error
    
    def clear(self):
        self.request_token = None
        self.access_token  = None
        self.verifier      = None

        self.request_token_secret = None
        self.access_token_secret = None
        
        self.request_oauth_nonce     = None
        self.request_oauth_timestamp = None
        self.access_oauth_nonce      = None
        self.access_oauth_timestamp  = None
        self.request_oauth_error     = None
        self.access_oauth_error      = None
