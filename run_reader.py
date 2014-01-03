#!/usr/bin/env python

from pybindxml import reader
import argparse

def main(): 
    parser = argparse.ArgumentParser(description='Parse BIND XML stats on demand.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--host',
                        help='hostname to query for DNS statistics')
    parser.add_argument('--port',
                        type=int,
                        default=8053,
                        help='BIND statistics port to query')
    parser.add_argument('--xml',
                        help='path to file which contains BIND XML.')                       
    args = parser.parse_args()

    if args.xml:
        mybind = reader.BindXmlReader(xml_path=args.xml)
    else:
        mybind = reader.BindXmlReader(host=args.host, port=args.port)

    mybind.get_stats()

    print "memory stats: %s" % mybind.stats.memory_stats
    print "query stats: %s" % mybind.stats.query_stats
    print "zone list: %s" % mybind.stats.zone_stats
    print "done"

if __name__ == '__main__':
    main()

