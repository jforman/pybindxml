"""Library to parse the various versions of BIND statstics XML."""

from bs4 import BeautifulSoup
try:
    from urllib.request import urlopen
    from urllib.error import URLError
except ImportError:
    from urllib2 import urlopen
    from urllib2 import URLError


class XmlError(Exception):
    """Base class of raising XML errors when reading BIND XML."""

    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class BindXmlReader(object):
    """Superclass for reading/processing BIND statistics XML."""

    def __init__(self, host=None, port=8053, xml_filepath=None):
        self.bs_xml = None
        self.host = host
        self.port = port
        self.raw_xml = None
        self.stats = None
        self.xml_filepath = xml_filepath
        self.xml_version = None

    def gather_xml(self):
        """Attempt to read the XML, whether from a file on-disk or via host:port.

        TODO: handle when you cant gather stats, due to bad hostname
        """
        if self.xml_filepath:
            with open(self.xml_filepath, "r") as xml_fh:
                self.raw_xml = xml_fh.read()
            self.bs_xml = BeautifulSoup(self.raw_xml, 'lxml')
        else:
            try:
                req = urlopen('http://%s:%s' % (self.host, self.port))
                self.raw_xml = req.read()
                self.bs_xml = BeautifulSoup(self.raw_xml, 'lxml')
            except URLError as u_error:
                raise XmlError('Unable to query BIND (%s:%s) for statistics. Reason: %s.' %
                               (self.host, self.port, u_error))

    def get_stats(self):
        """Given XML version, parse create XMLAbstract object and sets xml_stats attribute."""
        self.gather_xml()
        self.xml_version = self.bs_xml.find('statistics')['version']
        
        if self.xml_version is None:
            raise XmlError("Unable to determine XML version via 'statistics' tag.")

        if self.xml_version == '3.0':
            self.stats = XmlV30(self.bs_xml)
        elif self.xml_version == '3.3':
            self.stats = XmlV33(self.bs_xml)
        elif self.xml_version == '3.5':
            self.stats = XmlV35(self.bs_xml)
        elif self.xml_version == '3.6':
            self.stats = XmlV36(self.bs_xml)
        else:
            raise XmlError('Support must be added before being able to support newly-encountered XML version %s.' % self.xml_version)


class XmlAbstract(object):
    """Abstract class for the various XML versions to be parsed."""

    def __init__(self, xml):
        self.bs_xml = xml
        self.memory_stats = self.set_memory_stats()
        self.query_stats = self.set_query_stats()
        self.zone_stats = self.set_zone_stats()

    def set_memory_stats(self):
        """Return dict of memory counter and value for BIND process.

        Returns:
        Dict { memory_counter: Int value in bytes }
        """
        raise NotImplementedError('You must implement your own set_memory_stats method.')

    def set_query_stats(self):
        """Return a dict of query type and count from BIND statistics XML.

        Returns:
        Dict { query_type: Integer count }
        """
        raise NotImplementedError('You must implement your own set_query_stats method.')

    def set_zone_stats(self):
        """List the DNS zones and attributes.

        Returns:
        List of Dicts { String view_name,
        String zone_name,
        String zone_class,
        Int serial,
        Dict counters (which contains key/values for all counter values}
        """
        raise NotImplementedError('You must implement your own set_zone_stats method.')


class XmlV30(XmlAbstract):
    """Class for implementing methods for parsing BIND version 3.0 XML."""

    def __init__(self, xml):
        super(XmlV30, self).__init__(xml)

    def set_memory_stats(self):
        stats_dict = {}
        stats = self.bs_xml.find('memory').find('summary')
        for stat in stats.contents:
            if stat == '\n':
                continue
            if stat:
                stats_dict[stat.name] = int(stat.string)

        return stats_dict

    def set_query_stats(self):
        stats_dict = {}
        stats = self.bs_xml.find('server')
        for stat in stats.find(type='qtype'):
            if stat == '\n':
                continue
            stats_dict[stat['name']] = int(stat.string)
        for stat in stats.find(type='opcode'):
            if stat == '\n':
                continue
            stats_dict[stat['name']] = int(stat.string)

        return stats_dict

    def set_zone_stats(self):
        zone_dict = {}
        views = self.bs_xml.find_all('view')
        for view in views:
            for zone in view.find_all('zone'):
                if zone['rdataclass'] != 'IN':
                    continue
                zone_dict[zone['name']] = {}
                zone_dict[zone['name']][view['name']] = {}
                zone_dict[zone['name']][view['name']].update({
                        'serial': zone.find('serial').string
                        })
                counters = zone.find_all('counters')
                if counters:
                    for counter_type in counters:
                        # rcode, qtype, etc.
                        for counter in counter_type.find_all('counter'):
                            # UpdateDone, PTR, etc.
                            zone_dict[zone['name']][view['name']][counter['name']] = {}
                            zone_dict[zone['name']][view['name']][counter['name']].update({
                                'type': counter_type['type'],
                                'value': int(counter.string)})
        return zone_dict


class XmlV33(XmlV30):
    """Class for implementing methods for parsing BIND version 3.3 XML."""

    def __init__(self, xml):
        super(XmlV33, self).__init__(xml)


class XmlV35(XmlV30):
    """Class for implementing methods for parsing BIND version 3.5 XML."""

    def __init__(self, xml):
        super(XmlV35, self).__init__(xml)

    def set_query_stats(self):
        stats_dict = {}
        counter_stats = self.bs_xml.find('server').find_all('counters')
        for counter_group in counter_stats:
            # counter_type currently unused
            counter_type = counter_group['type']
            for counter in counter_group.find_all('counter'):
                stats_dict[counter['name']] = int(counter.string)

        return stats_dict

class XmlV36(XmlV30):
    """Class for implementing methods for parsing BIND version 3.5 XML."""

    def __init__(self, xml):
        super(XmlV36, self).__init__(xml)

    def set_query_stats(self):
        stats_dict = {}
        counter_stats = self.bs_xml.find('server').find_all('counters')
        for counter_group in counter_stats:
            # counter_type currently unused
            counter_type = counter_group['type']
            for counter in counter_group.find_all('counter'):
                stats_dict[counter['name']] = int(counter.string)

        return stats_dict
