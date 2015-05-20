#!/usr/bin/python

import urllib2
import csv
import gzip
import StringIO
from collections import Counter
import json

URL="http://software77.net/geo-ip/?DL=1"
FIELDS=["From","To","Registry","Assigned","Code","LongCode","Country"]

def index(c):
    return dict((v[0],i) for i,v in enumerate(c.most_common()))

def main():
    # data=StringIO.StringIO(open('IPLocations.csv.gz').read())
    data=StringIO.StringIO(urllib2.urlopen(URL).read())
    output=StringIO.StringIO()
    rows=[]
    previous=0
    starts=Counter()
    lengths=Counter()
    registrations=Counter()
    countries=Counter()
    for ip in csv.DictReader(gzip.GzipFile(fileobj=data),FIELDS):
        if not ip["From"].startswith("#"):
            start=int(ip["From"])-previous
            length=int(ip["To"])-int(ip["From"])+1
            registration=int(ip["Assigned"])/100
            code=ip["LongCode"]
            starts[start]+=1
            lengths[length]+=1
            registrations[registration]+=1
            countries[code]+=1
            rows.append([start,length,registration,code])
            previous=int(ip["To"])+1
    starts=index(starts)
    lengths=index(lengths)
    registrations=index(registrations)
    countries=index(countries)
    output.write("|".join("%x,%x,%x,%x"%(starts[row[0]],lengths[row[1]],registrations[row[2]],countries[row[3]]) for row in rows))
    json.dump({
        "starts"        : sorted(starts, key=starts.get),
        "lengths"       : sorted(lengths, key=lengths.get),
        "registrations" : sorted(registrations, key=registrations.get),
        "countries"     : sorted(countries, key=countries.get),
        "data"          : output.getvalue()
    },open("ips.json","w+"))

if __name__ == '__main__':
    main()