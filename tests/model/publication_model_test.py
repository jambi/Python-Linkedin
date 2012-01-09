import unittest
from linkedin.model import *

class PublicationModelTest(unittest.TestCase):

    def test_simple(self):
        xml = """
        <publication>
            <id>3</id>
            <title>Publication list, with links to individual papers</title>
            <publisher>
                <name>Iftach</name>
            </publisher>
            <date>
                <year>2005</year>
                <month>5</month>
            </date>
            <url>URLURL</url>
            <summary>My summary</summary>
        </publication>
        """

        pub = Publication.create(minidom.parseString(xml))
        self.assertEquals("3", pub.id)
        self.assertEquals("Publication list, with links to individual papers", pub.title)
        self.assertEquals("Iftach", pub.publisher_name)
        self.assertEquals(datetime.date(2005, 5, 1), pub.date)
        self.assertEquals("URLURL", pub.url)
        self.assertEquals("My summary", pub.summary)
        
    # TODO Give up on authors until someone will request it