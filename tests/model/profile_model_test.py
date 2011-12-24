import unittest
from linkedin.model import *
from xml.dom import minidom

class ProfileModelTest(unittest.TestCase):

    def test_real_example(self):
        xml = open("example.xml", "r").read()
        p = Profile.create(minidom.parseString(xml))

        self.assertEquals(0, p.num_recommenders)
        self.assertEquals("sqvX__QhX3", p.id)
        self.assertEquals("Software Team Leader at XIV", p.headline)
        self.assertEquals(False, p.num_connections_capped)
        self.assertEquals(3, p.num_connections)
        self.assertEquals("Iftach", p.first_name)
        self.assertEquals("Bar", p.last_name)
        self.assertEquals(0, p.distance)
        self.assertEquals("http://www.linkedin.com/pub/iftach-bar/23/a38/a69", p.public_profile_url)
        
        "three-current-positions"
        "connections"
        "member-url-resources"
        "phone-numbers"
        "location"
        "educations"
        "recommendations-received"
        "twitter-accounts"
        "three-past-positions"
        "relation-to-viewer"
        "skills"
        "positions"
        "im-accounts"
        "api-standard-profile-request"
        "site-standard-profile-request"

    def test_relation_to_viewer(self):
        xml = """
        <?xml version="1.0" ?><person>
  <relation-to-viewer>
    <distance>1</distance>
    <connections count="2" start="0" total="2">
      <connection>
        <person>
          <id>xig-q-864a</id>
          <first-name>Shem</first-name>
          <last-name>Magnezi</last-name>
        </person>
      </connection>
      <connection>
        <person>
          <id>JBhVscvmlT</id>
          <first-name>amir</first-name>
          <last-name>boldo</last-name>
        </person>
      </connection>
    </connections>
  </relation-to-viewer>
</person>
        """
        p = Profile.create(xml)
        self.assertTrue(p.relation_to_viewer)
        
        
        


