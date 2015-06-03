from pybindxml import reader
import unittest

class Test_v22(unittest.TestCase):
    def setUp(self):
        self.xml_obj = reader.BindXmlReader(xml_filepath='testdata/bindxml-v2_2.xml')
        self.xml_obj.get_stats()

    def test_objectCreation(self):
        '''Ensure we can create the BindXmlReader object, and properly read the XML.'''
        self.assertEqual(type(self.xml_obj), reader.BindXmlReader)
        self.assertEqual(type(self.xml_obj.stats), reader.XmlV22)

    def test_ExpectedZoneCount(self):
        """Ensure we are parsing the expected number of zones in the XML file."""
        self.assertEqual(len(list(self.xml_obj.stats.zone_stats.keys())), 5)

    def test_ZoneStats(self):
        """Ensure we can read various levels of stats for a particular zone."""
        zone_list = self.xml_obj.stats.zone_stats
        self.assertEqual(zone_list['dom1.example.org']['_default']['serial'], '266')
        self.assertEqual(zone_list['dom1.example.org']['_default']['qrysuccess']['value'], 11508)

    def test_MemoryStats(self):
        """Ensure the memory stats we're expecting are populated."""
        memory_stats = self.xml_obj.stats.memory_stats
        self.assertEqual({'totaluse': 29580570,
                          'inuse': 2781108,
                          'blocksize': 28311552,
                          'contextsize': 5902032,
                          'lost': 0},
                         memory_stats)

    def test_QueryStats(self):
        """Ensure we are counting the number of queries expectedly."""
        query_stats = self.xml_obj.stats.query_stats
        self.assertEqual(query_stats['QUERY'], 4889434)
        self.assertEqual(query_stats['A'], 4108334)

if __name__ == '__main__':
    unittest.main()
