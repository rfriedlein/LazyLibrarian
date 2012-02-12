import time, threading, urllib, urllib2, re

from xml.etree import ElementTree

import lazylibrarian

from lazylibrarian import logger


def NewzNab(searchlist=None):

    HOST = lazylibrarian.NEWZNAB_HOST
    results = []

    for searchterm in searchlist:
        logger.info('Searching for %s.' % searchterm['searchterm'])
        params = {
            "t": "search",
            "apikey": lazylibrarian.NEWZNAB_API,
            "cat": 7020,
            "q": searchterm['searchterm']
            }

        if not str(HOST)[:4] == "http":
            HOST = 'http://' + HOST

        URL = HOST + '/api?' + urllib.urlencode(params)

        try:
            data = ElementTree.parse(urllib2.urlopen(URL, timeout=30))
        except (urllib2.URLError, IOError, EOFError), e:
            logger.warn('Error fetching data from %s: %s' % (lazylibrarian.NEWZNAB_HOST, e))
            data = None

        if data:
            # to debug because of api
            logger.debug(u'Parsing results from <a href="%s">%s</a>' % (URL, lazylibrarian.NEWZNAB_HOST))
            rootxml = data.getroot()
            resultxml = rootxml.getiterator('item')
            nzbcount = 0
            for nzb in resultxml:
                nzbcount = nzbcount+1
                results.append({
                    'bookid': searchterm['bookid'],
                    'nzbprov': "NewzNab",
                    'nzbtitle': nzb[0].text,
                    'nzburl': nzb[2].text,
                    'nzbdate': nzb[4].text,
                    'nzbsize': nzb[7].attrib.get('length')
                    })
                logger.info('Found %s nzb for: %s' % (nzbcount, searchterm['searchterm']))
        time.sleep(1)
    return results

