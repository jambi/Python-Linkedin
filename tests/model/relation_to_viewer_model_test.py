import unittest
from linkedin.model import *

class RelationToViewerModelTest(unittest.TestCase):
    def test_empty(self):
        # TODO fill this in
        pass
    
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
        r = RelationToViewer(node)
        self.assertEquals(2, r.distance)
        self.assertEquals(1, r.num_related_connections)
#        self.assertEquals(1, r.conn)
        
    