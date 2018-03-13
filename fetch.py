# -*- coding: utf-8 -*-

import requests
import xml.etree.ElementTree as ET

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
            #print(mesume)
            museumId = museum['Id']
            #if museumId in museums:
            #    print(museums[museumId])
            #    print(museum)
            museums[museumId] = museum

        params['start'] += params['count']
        print(len(museums))

if __name__ == '__main__':
    fetchMuseums()

