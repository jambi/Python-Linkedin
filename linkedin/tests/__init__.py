import unittest

API_KEY = "wFNJekVpDCJtRPFX812pQsJee-gt0zO4X5XmG6wcfSOSlLocxodAXNMbl0_hw3Vl"
SECRET_KEY = "daJDa6_8UcnGMw1yuq9TjoO_PMKukXMo8vEMo7Qv5J-G3SPgrAV0FqFCd0TNjQyG"
RETURN_URL = "http://localhost:8000"

class LinkedInTestBase(unittest.TestCase):
    
    @classmethod
    def _create_http_server(cls, api):
        import BaseHTTPServer
        class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
            def do_GET(self):
                p = self.path.split("?")
                params = {}
                if len(p) > 1:
                    import cgi
                    params = cgi.parse_qs(p[1], True, True)
                    api._verifier = params["oauth_verifier"][0]

        server_address = ('', 8000)
        cls.httpd = BaseHTTPServer.HTTPServer(server_address, MyHandler)
        
    @classmethod
    def _init_gae(cls):
        from google.appengine.api import apiproxy_stub_map
        from google.appengine.api import urlfetch_stub
        apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap() 
        apiproxy_stub_map.apiproxy.RegisterStub('urlfetch', urlfetch_stub.URLFetchServiceStub())