from pybindxml import reader
import unittest

class Tests_v36(unittest.TestCase):
    def setUp(self):
        self.xml_obj = reader.BindXmlReader(xml_filepath='testdata/bindxml-v3_6.xml')
        self.xml_obj.get_stats()

    def test_objectCreation(self):
        """Ensure we can create the BindXmlReader object, and properly read the XML."""
        self.assertEqual(type(self.xml_obj), reader.BindXmlReader)
        self.assertEqual(type(self.xml_obj.stats), reader.XmlV36)
    
    def test_ExpectedZoneCount(self):
        """Ensure we are parsing the expected number of zones in the XML file."""
        self.assertEqual(len(list(self.xml_obj.stats.zone_stats.keys())), 103)
        
    def test_ZoneStats(self):
        """Ensure we can read various levels of stats for a particular zone."""
        dom1 = self.xml_obj.stats.zone_stats['2.10.10.in-addr.arpa']
        self.assertEqual(dom1['_default']['serial'], '12')
        self.assertEqual(dom1['_default']['QrySuccess']['value'], 59)

    def test_MemoryStats(self):
        """Ensure the memory stats we're expecting are populated."""
        memory_stats = self.xml_obj.stats.memory_stats
        self.assertEqual({'totaluse': 550974137,
                          'inuse': 12430640,
                          'blocksize': 51904512,
                          'contextsize': 8479392,
                          'lost': 0},
                         memory_stats)

    def test_QueryStats(self):
        """Ensure we are counting the number of queries expectedly."""
        query_stats = self.xml_obj.stats.query_stats
        self.assertEqual(query_stats['A'], 1962798)
        self.assertEqual(query_stats['QUERY'], 3719262)


if __name__ == '__main__':
    unittest.main()
