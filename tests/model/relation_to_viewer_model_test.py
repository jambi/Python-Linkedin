import unittest
from linkedin.model import *

class RelationToViewerModelTest(unittest.TestCase):
    def test_empty(self):
        xml = """
        <relation-to-viewer>
            <distance>0</distance>
            <connections total="0" count="0" start="0">
            </connections>
            <num-related-connections>0</num-related-connections>
        </relation-to-viewer>
        """
        node = minidom.parseString(xml)
        r = RelationToViewer.create(node)
        self.assertEquals(0, r.distance)
        self.assertEquals(0, r.num_related_connections)
        self.assertEquals(0, len(r.connections))

    def test_empty2(self):
        xml = """
        <relation-to-viewer>
            <distance>0</distance>
            <num-related-connections>0</num-related-connections>
        </relation-to-viewer>
        """
        node = minidom.parseString(xml)
        r = RelationToViewer.create(node)
        self.assertEquals(0, r.distance)
        self.assertEquals(0, r.num_related_connections)
        self.assertEquals(0, len(r.connections))


    def test_full(self):
        xml = """
        <relation-to-viewer>
            <distance>2</distance>
            <connections total="1" count="10" start="0">
                <connection>
                    <person>
                        <id>_tQbzI5kEk</id>
                        <first-name>Michael</first-name>
                        <last-name>Green</last-name>
                    </person>
                </connection>
            </connections>
            <num-related-connections>1</num-related-connections>
        </relation-to-viewer>
        """
        node = minidom.parseString(xml)
        r = RelationToViewer.create(node)
        self.assertEquals(2, r.distance)
        self.assertEquals(1, r.num_related_connections)
        self.assertEquals(1, len(r.connections))
        connection = r.connections[0]
        self.assertEquals("Michael", connection.first_name)
        self.assertEquals("Green", connection.last_name)
        self.assertEquals("_tQbzI5kEk", connection.id)

        
    