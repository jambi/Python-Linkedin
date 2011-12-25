import unittest
from linkedin.model import *

class PositionModelTest(unittest.TestCase):

    def test_simple(self):
        xml = """
    <position>
      <id>182283292</id>
      <title>Software Team Leader</title>
      <summary>Python team leader</summary>
      <start-date>
        <year>2010</year>
        <month>10</month>
      </start-date>
      <is-current>true</is-current>
      <company>
        <id>1009</id>
        <name>XIV - IBM</name>
        <type>Public Company</type>
        <industry>Information Technology and Services</industry>
        <ticker>IBM</ticker>
      </company>
    </position>
        """
        position = Position.create(minidom.parseString(xml))

        self.assertEquals("182283292", position.id)
        self.assertEquals("Software Team Leader", position.title)
        self.assertEquals("Python team leader", position.summary)
        self.assertEquals(datetime.date(2010, 10, 1), position.start_date)
        self.assertEquals(True, position.is_current)
        self.assertIsInstance(position.company, Company)
        