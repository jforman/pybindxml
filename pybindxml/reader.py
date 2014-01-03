""" Library to parse the various versions of BIND statstics XML."""

from bs4 import BeautifulSoup
import urllib2

class XmlError(Exception):
    """ Base class of raising XML errors when reading BIND XML."""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class BindXmlReader(object):
    """Superclass for reading/processing BIND statistics XML."""

    def __init__(self, host=None, port=8053, xml_filepath=None):
        self.host = host
        self.port = port
        self.bs_xml = None
        self.raw_xml = None
        self.xml_filepath = xml_filepath
        self.xml_stats = None
        self.xml_version = None
        self.set_xml_version()
        self.get_xml_stats()

    def get_xml(self):
        """ Attempt to read the XML, whether from a file on-disk or via host:port."""
        if self.xml_filepath:
            with open(self.xml_filepath, "r") as xml_fh:
                self.raw_xml = xml_fh.read()
            self.bs_xml = BeautifulSoup(self.raw_xml)
        else:
            try:
                req = urllib2.urlopen('http://%s:%s' % (self.host, self.port))
                self.raw_xml = req.read()
                self.bs_xml = BeautifulSoup(self.raw_xml, 'xml')
            except urllib2.URLError, u_error:
                raise XmlError('Unable to query BIND (%s) for statistics. Reason: %s.',
                               self.host,
                               u_error)

    def get_xml_version(self):
        """ Get XML version of BIND statistics XML."""
        return self.xml_version

    def set_xml_version(self):
        """ Run this after init'ing to attempt to read XML and determine version
        of XML for later processing."""
        self.get_xml()
        self.xml_version = self.bs_xml.find('statistics')['version']
        
        if self.xml_version is None:
            raise XmlError("Unable to determine XML version via 'statistics' tag.")

    def get_xml_stats(self):
        """ Given XML version, parse create XMLAbstract object and sets xml_stats attribute."""
        if self.xml_version == '2.2':
            self.xml_stats = XmlV22(self.bs_xml)
        elif self.xml_version == '3.0':
            self.xml_stats = XmlV30(self.bs_xml)
        else:
            raise XmlError('Not configured to handle XML version %s.' % self.xml_version)


class XmlAbstract(object):
    """ Abstract class for the various XML versions to be parsed. """
    def __init__(self, xml):
        self.bs_xml = xml
        self.memory_stats = self.get_memory_stats()
        self.query_stats = self.get_query_stats()
        self.zone_stats = self.get_zone_stats()

    def get_memory_stats(self):
        """ Return dict of memory counter and value for BIND process.

        Returns:
        Dict { memory_counter: Int value in bytes }
        """
        raise NotImplementedError('You must implement your own get_memory_stats method.')

    def get_query_stats(self):
        """ Return a dict of query type and count from BIND statistics XML.

        Returns:
        Dict { query_type: Integer count }
        """
        raise NotImplementedError('You must implement your own get_query_stats method.')

    def get_zone_stats(self):
        """ List the DNS zones and attributes.

        Returns:
        List of Dicts { String view_name,
        String zone_name,
        String zone_class,
        Int serial,
        Dict counters (which contains key/values for all counter values}
        """
        raise NotImplementedError('You must implement your own get_zone_stats method.')


class XmlV22(XmlAbstract):
    """Class for implementing methods for parsing BIND version 2.2 XML."""
    def __init__(self, xml):
        super(self.__class__, self).__init__(xml)

    def get_memory_stats(self):
        stats_dict = {}
        stats = self.bs_xml.find('bind').find('statistics').find('memory').find('summary')
        for stat in stats.contents:
            if stat == u'\n':
                continue
            if stat:
                stats_dict[stat.name] = int(stat.string)

        return stats_dict

    def get_query_stats(self):
        stats_dict = {}
        stats = self.bs_xml.find('server')
        for stat in stats.find('queries-in'):
            if stat == u'\n':
                continue
            if stat:
                stats_dict[stat.find('name').string] = int(stat.find('counter').string)

        for stat in stats.find_all('opcode'):
            if stat == u'\n':
                continue
            if stat:
                stats_dict[stat.find('name').string] = int(stat.find('counter').string)

        return stats_dict

    def get_zone_stats(self):
        zone_list = []
        views = self.bs_xml.find('views').find_all('view')
        for view in views:
            view_name = view.find('name').string
            for zone in view.findAll('zone'):
                zone_name, zone_class = zone.find('name').string.split('/')
                serial = int(zone.find('serial').string)
                zone_dict = {}
                if zone_class != 'IN':
                    continue
                zone_dict.update({'view' : view_name,
                                  'zone' : zone_name,
                                  'class' : zone_class,
                                  'serial' : serial })
                zone_dict['counters'] = {}
                counters = zone.find('counters')
                for counter in counters.children:
                    if counter == u'\n':
                        continue
                    zone_dict['counters'][counter.name] = counter.string
                zone_list.append(zone_dict)
            
        return zone_list

class XmlV30(XmlAbstract):
    """Class for implementing methods for parsing BIND version 3.0 XML."""
    def __init__(self, xml):
        super(self.__class__, self).__init__(xml)

    def get_memory_stats(self):
        stats_dict = {}
        stats = self.bs_xml.find('memory').find('summary')
        for stat in stats.contents:
            if stat == u'\n':
                continue
            if stat:
                stats_dict[stat.name] = int(stat.string)

        return stats_dict

    def get_query_stats(self):
        stats_dict = {}
        stats = self.bs_xml.find('server')
        for stat in stats.find(type='qtype'):
            stats_dict[stat['name']] = int(stat.string)
        for stat in stats.find(type='opcode'):
            stats_dict[stat['name']] = int(stat.string)

        return stats_dict

    def get_zone_stats(self):
        zone_list = []
        views = self.bs_xml.find('views')
        for view in views:
            for zone in view.find_all(rdataclass='IN'):
                zone_dict = {}
                zone_dict.update({'view': view['name'],
                                  'zone': zone['name'],
                                  'serial': zone.find('serial').string})
                zone_dict['counters'] = {}
                counters = zone.find_all('counter')
                for counter in counters:
                    zone_dict['counters'][counter['name']] = int(counter.string)
                zone_list.append(zone_dict)

        return zone_list
