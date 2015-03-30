from pybindxml import reader
import unittest

class Tests_v30(unittest.TestCase):
    def setUp(self):
        self.xml_obj = reader.BindXmlReader(xml_filepath='testdata/bindxml-v3_0.xml')
        self.xml_obj.get_stats()

    def test_objectCreation(self):
        """Ensure we can create the BindXmlReader object, and properly read the XML."""
        self.assertEqual(type(self.xml_obj), reader.BindXmlReader)
        self.assertEqual(type(self.xml_obj.stats), reader.XmlV30)
    
    def test_ExpectedZoneCount(self):
        """Ensure we are parsing the expected number of zones in the XML file."""
        self.assertEqual(len(list(self.xml_obj.stats.zone_stats.keys())), 104)
        
    def test_ZoneStats(self):
        """Ensure we can read various levels of stats for a particular zone."""
        dom1 = self.xml_obj.stats.zone_stats['dom1.example.org']
        self.assertEqual(dom1['_default']['serial'], 1803)
        self.assertEqual(dom1['_default']['QrySuccess']['value'], 87224)

    def test_MemoryStats(self):
        """Ensure the memory stats we're expecting are populated."""
        memory_stats = self.xml_obj.stats.memory_stats
        self.assertEqual({'totaluse': 34342237,
                          'inuse': 9677495,
                          'blocksize': 30146560,
                          'contextsize': 5593640,
                          'lost': 0},
                         memory_stats)

    def test_QueryStats(self):
        """Ensure we are counting the number of queries expectedly."""
        query_stats = self.xml_obj.stats.query_stats
        self.assertEqual(query_stats['A'], 157431)
        self.assertEqual(query_stats['QUERY'], 269977)


if __name__ == '__main__':
    unittest.main()
