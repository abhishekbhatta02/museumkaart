# -*- coding: utf-8 -*-

import requests
import xml.etree.ElementTree as ET
import json
from html.parser import HTMLParser

class SimpleParser(HTMLParser):
    latitude = None
    longitude = None
    mapUrl = None
    def handle_starttag(self, tag, attrs):
        isMap = 0
        mapUrl = ''
        for (attr,value) in attrs:
            if attr == 'class' and 'important-link--location' in value:
                isMap += 1
            if attr == 'href':
                isMap += 1
                mapUrl = value
            if isMap > 1:
                break
        if isMap > 1:
            latitude, longitude = mapUrl.split('%40')[1].split('&')[0].split(',')

            self.mapUrl = mapUrl
            self.latitude = latitude
            self.longitude = longitude

    def handle_endtag(self, tag):
        pass
    def handle_data(self, data):
        pass

def fetchMuseums():
    print('fetch')
    museums = {}
    params = {'start':0, 'count':31}
    url = 'https://www.museumkaart.nl/Services/SchatkamerService.svc/GetSchatkamerKaart'
    jar = {}
    #'https://www.museumkaart.nl/Services/SchatkamerService.svc/GetMuseumSchatkamerKaarten?&start=0&count=28&museumId=123&id=12579&showNotFound=false'

    while True:
        ns = {'data': 'http://schemas.microsoft.com/ado/2007/08/dataservices' }
        print(params)
        r = requests.get(url, params=params, cookies=jar)
        jar = r.cookies
        root = ET.fromstring(r.text)
        if len(list(root)) == 0:
            break
        for museumElement in root:
            attributes = list(museumElement)
            museum = {}
            for attribute in attributes:
                tagName = attribute.tag[len(ns['data']) + 2:]
                tagValue = attribute.text
                museum[tagName] = tagValue
            museumId = museum['Id']
            if museumId in museums:
                pass
                #print(museums[museumId])
            else:
                fetchDetail(museum)
            #print(museum)
            museums[museumId] = museum

        params['start'] += params['count']
        print(len(museums))

    f = open('museums.json', 'w')
    f.write(json.dumps(museums))
    f.close()

def fetchDetail(museum):
    print(museum['DetailUrl'])
    url = 'https://www.museumkaart.nl' + museum['DetailUrl']
    r = requests.get(url)
    parser = SimpleParser()
    parser.feed(r.text)
    museum['Longitude'] = parser.longitude
    museum['Latitude'] = parser.latitude
    museum['MapUrl'] = parser.mapUrl

    f = open('museums/' + museum['Id'] + '.json', 'w')
    f.write(json.dumps(museum))
    f.close()

if __name__ == '__main__':
    fetchMuseums()

