py-bindxml
==========

[![Build Status](https://travis-ci.org/jforman/pybindxml.svg?branch=master)](https://travis-ci.org/jforman/pybindxml)
[![Code Health](https://landscape.io/github/jforman/pybindxml/master/landscape.svg?style=flat)](https://landscape.io/github/jforman/pybindxml/master)

Library to handle parsing BIND statistics XML into Python objects.

Data Structure
--------------
Memory Statistics:
```
{'<Memory Type>': int(value in bytes), ...}
```

Query Statistics:
```
{'<Query RR Type>': int(number of queries), ...}
```

Zone Statistics:
```
{'<Domain Name>': {
    '<View Name1>': {
        '<Request Type1>': {
            '<request category>': unicode(category name),
            '<value>': int(number of requests)
        },
        '<Request Type2>': {
            '<request category>': unicode(category name),
            '<value>': int(number of requests)
        },
        ....
    }
}
```



Typical Usage
-------------
```
>>> from pybindxml import reader
>>> foo = reader.BindXmlReader(host='mybindhost')
>>> foo.get_stats()
>>> foo.stats.query_stats
{u'A': 1625230, u'SOA': 300, u'DS': 38, u'UPDATE': 50, u'MX': 4, u'AAAA': 1115994, u'DNSKEY': 38, u'QUERY': 2750728, u'TXT': 46, u'PTR': 9078}
>>> foo.stats.memory_stats
{'BlockSize': 40632320, 'InUse': 11451124, 'ContextSize': 6925480, 'Lost': 0, 'TotalUse': 45022170}
>>> foo.stats.zone_stats.keys()
[u'0.20.10.in-addr.arpa', u'24.172.IN-ADDR.ARPA', u'118.100.IN-ADDR.ARPA', u'dom1.example.org', u'25.172.IN-ADDR.ARPA', u'22.172.IN-ADDR.ARPA', u'77.100.IN-ADDR.ARPA', u'83.100.IN-ADDR.ARPA',....]
>>> foo.stats.zone_stats['dom1.example.org'].keys()
[u'_default']
>>> foo.stats.zone_stats['dom1.example.org']['_default'].keys()
[u'ReqBadEDNSVer', u'Requestv6', u'ReqSIG0', u'XfrRej', u'AAAA', u'QryNXDOMAIN', 'serial', u'ReqBadSIG', u'RPZRewrites', u'QrySuccess', u'QryAuthAns', u'UpdateRespFwd', u'AuthQryRej', u'QryFailure', u'UpdateRej', u'Response',....]
>>> foo.stats.zone_stats['dom1.example.org']['_default']['serial']
1803
>>> foo.stats.zone_stats['dom1.example.org']['_default']['A']
{'type': u'qtype', 'value': 937710}
>>> foo.stats.zone_stats['dom1.example.org']['_default']['A']['value']
937710
```

