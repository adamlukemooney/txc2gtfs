import csv
import xml.etree.ElementTree
import os
import sys

from models.Route import Route
from extractors.Mappings import txcmodetogtfstype

class RouteExtractor:
  PRINT_PROGRESS_INTERVAL = 0.1
  TXC_NAMESPACES = {'txc': 'http://www.transxchange.org.uk/'}

  inputfiles = os.listdir('input')
  totalfiles = len(inputfiles)
  progress = 0.0
  routes = []

  def extract(self):
    print "Extracting routes from input directory"
    self.__extractroutes()
    self.__writegtfsroutes()
    print "- Done"

  def __extractroutes(self):
    sys.stdout.write('- Reading TXC Services+Lines to GTFS Routes in memory')
    sys.stdout.flush()
    for index, file in enumerate(self.inputfiles):
      self.__printprogress(index)
      if file.endswith('.xml'):
        self.__process(file)
    print "."

  def __printprogress(self, currentindex):
    if(currentindex / float(self.totalfiles) > self.progress + self.PRINT_PROGRESS_INTERVAL):
      sys.stdout.write('.')
      sys.stdout.flush()
      self.progress += 0.1

  def __process(self, file):
    for service in self.__getservices(file):
      for line in service.findall('txc:Lines/txc:Line', self.TXC_NAMESPACES):
        self.routes.append(self.__convertserviceandlinetoroute(service, line))

  def __convertserviceandlinetoroute(self, service, line):
    routeid = line.attrib['id']
    routename = line.find('txc:LineName', self.TXC_NAMESPACES).text
    txcmode = service.find('txc:Mode', self.TXC_NAMESPACES).text
    routetype = txcmodetogtfstype(txcmode)
    agencyid = service.find('txc:RegisteredOperatorRef', self.TXC_NAMESPACES).text
    return Route(routeid, agencyid, routename, routetype)

  def __getservices(self, file):
    root = xml.etree.ElementTree.parse('input/' + file).getroot()
    return root.findall('txc:Services/txc:Service', self.TXC_NAMESPACES)

  def __writegtfsroutes(self):
    print "- Writing routes.txt"
    with open('output/routes.txt', 'wb') as csvfile:
      csvwriter = csv.writer(csvfile)
      csvwriter.writerow(['route_id', 'agency_id', 'route_short_name', 'route_long_name', 'route_type'])
      for route in self.routes:
        csvwriter.writerow(route.getgtfsvalues())
