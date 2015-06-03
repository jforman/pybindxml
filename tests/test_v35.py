from pybindxml import reader
import unittest

class Tests_v35(unittest.TestCase):
    def setUp(self):
        self.xml_obj = reader.BindXmlReader(xml_filepath='testdata/bindxml-v3_5.xml')
        self.xml_obj.get_stats()

    def test_objectCreation(self):
        """Ensure we can create the BindXmlReader object, and properly read the XML."""
        self.assertEqual(type(self.xml_obj), reader.BindXmlReader)
        self.assertEqual(type(self.xml_obj.stats), reader.XmlV35)
    
    def test_ExpectedZoneCount(self):
        """Ensure we are parsing the expected number of zones in the XML file."""
        self.assertEqual(len(self.xml_obj.stats.zone_stats.keys()), 105)
        
    def test_ZoneStats(self):
        """Ensure we can read various levels of stats for a particular zone."""
        dom1 = self.xml_obj.stats.zone_stats['2.10.10.in-addr.arpa']
        self.assertEqual(dom1['_default']['serial'], '10')
        self.assertEqual(dom1['_default']['QrySuccess']['value'], 4)

    def test_MemoryStats(self):
        """Ensure the memory stats we're expecting are populated."""
        memory_stats = self.xml_obj.stats.memory_stats
        self.assertEqual({'totaluse': 54552872,
                          'inuse': 11639576,
                          'blocksize': 50855936,
                          'contextsize': 8523744,
                          'lost': 0},
                         memory_stats)

    def test_QueryStats(self):
        """Ensure we are counting the number of queries expectedly."""
        query_stats = self.xml_obj.stats.query_stats
        self.assertEqual(query_stats['A'], 392335)
        self.assertEqual(query_stats['QUERY'], 477126)


if __name__ == '__main__':
    unittest.main()
