from tests.linkedin_test import LinkedInMethodsTestBase
from tests import LinkedInTestBase

class LinkedInGaeTest(LinkedInMethodsTestBase, LinkedInTestBase):
    
    @classmethod
    def setUpClass(cls):
        cls._init_gae()
        cls.set_up_class(True)