import unittest
from linkedin.model import *

class CompanyModelTest(unittest.TestCase):

    def test_simple(self):
        xml = """
        <company>
        <id>1009</id>
        <name>XIV - IBM</name>
        <type>Public Company</type>
        <size>123</size>
        <industry>Information Technology and Services</industry>
        <ticker>IBM</ticker>
        </company>
        """
        company = Company.create(minidom.parseString(xml))
        self.assertEquals("1009", company.id)
        self.assertEquals("XIV - IBM", company.name)
        self.assertEquals("Public Company", company.type)
        self.assertEquals("123", company.size)
        self.assertEquals("Information Technology and Services", company.industry)
        self.assertEquals("IBM", company.ticker)
        
        