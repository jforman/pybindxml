import reader
import unittest

class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        self.xml_obj = reader.BindXmlReader(xml_filepath='testdata/bindxml-v2_2.xml')
        self.xml_obj.gather_xml()
        self.xml_obj.set_stats()

    def test_objectCreation(self):
        '''Ensure we can create the BindXmlReader object, and properly read the XML.'''
        self.assertEqual(type(self.xml_obj), reader.BindXmlReader)

    def test_ZoneStats(self):
        zone_list = self.xml_obj.stats.zone_stats
        self.assertEqual(len(zone_list), 4)
        for test_zone in zone_list:
            if test_zone['zone'] == 'dom1.example.org':
                data = test_zone
                break
        self.assertEqual(data['serial'], 266)
        self.assertEqual(data['counters']['qrysuccess'], u'11508')

    def test_MemoryStats(self):
        memory_stats = self.xml_obj.stats.memory_stats
        self.assertEqual({'totaluse': 29580570,
                              'inuse': 2781108,
                              'blocksize': 28311552,
                              'contextsize': 5902032,
                              'lost': 0},
                             memory_stats)


if __name__ == '__main__':
    unittest.main()
