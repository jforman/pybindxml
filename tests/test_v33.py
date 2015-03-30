from pybindxml import reader
import unittest

class Tests_v33(unittest.TestCase):
    def setUp(self):
        self.xml_obj = reader.BindXmlReader(xml_filepath='testdata/bindxml-v3_3.xml')
        self.xml_obj.get_stats()

    def test_objectCreation(self):
        """Ensure we can create the BindXmlReader object, and properly read the XML."""
        self.assertEqual(type(self.xml_obj), reader.BindXmlReader)
        self.assertEqual(type(self.xml_obj.stats), reader.XmlV33)
    
    def test_ExpectedZoneCount(self):
        """Ensure we are parsing the expected number of zones in the XML file."""
        self.assertEqual(len(list(self.xml_obj.stats.zone_stats.keys())), 102)
        
    def test_ZoneStats(self):
        """Ensure we can read various levels of stats for a particular zone."""
        dom1 = self.xml_obj.stats.zone_stats['homenet.mydomain.net']
        self.assertEqual(dom1['_default']['serial'], 1860)
        self.assertEqual(dom1['_default']['QrySuccess']['value'], 539687)

    def test_MemoryStats(self):
        """Ensure the memory stats we're expecting are populated."""
        memory_stats = self.xml_obj.stats.memory_stats
        self.assertEqual({'totaluse': 46118122,
                          'inuse': 11354788,
                          'blocksize': 41680896,
                          'contextsize': 7280584,
                          'lost': 0},
                         memory_stats)

    def test_QueryStats(self):
        """Ensure we are counting the number of queries expectedly."""
        query_stats = self.xml_obj.stats.query_stats
        self.assertEqual(query_stats['A'], 975811)
        self.assertEqual(query_stats['QUERY'], 1798801)


if __name__ == '__main__':
    unittest.main()
