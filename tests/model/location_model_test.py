import unittest
from linkedin.model import *

class LocationModelTest(unittest.TestCase):
    
    def test_location(self):
        xml = """
        <location>
            <name>Israel</name>
            <country>
                <code>il</code>
            </country>
        </location>
        """
        node = minidom.parseString(xml)
        l = Location.create(node)
        self.assertEquals("Israel", l.name)
        self.assertEquals("il", l.country_code)
        
    def test_empty_location(self):
        xml = """
        <location>
        </location>
        """
        node = minidom.parseString(xml)
        l = Location.create(node)
        self.assertEquals(None, l.name)
        self.assertEquals(None, l.country_code)
        
    def test_partial_location(self):
        xml = """
        <location>
            <name>Israel</name>
            <country>
            </country>
        </location>
        """
        node = minidom.parseString(xml)
        l = Location.create(node)
        self.assertEquals("Israel", l.name)
        self.assertEquals(None, l.country_code)
        
    def test_partial_location2(self):
        xml = """
        <location>
            <name>Israel</name>
        </location>
        """
        node = minidom.parseString(xml)
        l = Location.create(node)
        self.assertEquals("Israel", l.name)
        self.assertEquals(None, l.country_code)
        
    def test_partial_location3(self):
        xml = """
        <location>
            <country>
                <code>il</code>
            </country>
        </location>
        """
        node = minidom.parseString(xml)
        l = Location.create(node)
        self.assertEquals(None, l.name)
        self.assertEquals("il", l.country_code)
        