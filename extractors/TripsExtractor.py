import csv
import xml.etree.ElementTree
import os
import sys

from models.Trip import Trip

class TripsExtractor:
  PRINT_PROGRESS_INTERVAL = 0.1
  TXC_NAMESPACES = {'txc': 'http://www.transxchange.org.uk/'}

  inputfiles = os.listdir('input')
  totalfiles = len(inputfiles)
  progress = 0.0
  trips = []

  def extract(self):
    print "Extracting trips from input directory"
    self.__extracttrips()
    self.__writegtfstrips()
    print "- Done"

  def __extracttrips(self):
    sys.stdout.write('- Reading TXC VehicleJourneys to GTFS trips in memory')
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
    xmlroot = xml.etree.ElementTree.parse('input/' + file).getroot()
    for vehiclejourney in self.__getvehiclejourneys(xmlroot):
      self.trips.append(self.__convertvehiclejourneytotrip(xmlroot, vehiclejourney))

  def __convertvehiclejourneytotrip(self, xmlroot, vehiclejourney):
    tripid = vehiclejourney.find('txc:VehicleJourneyCode', self.TXC_NAMESPACES).text
    serviceid = tripid
    routeid = vehiclejourney.find('txc:LineRef', self.TXC_NAMESPACES).text
    txcserviceref = vehiclejourney.find('txc:ServiceRef', self.TXC_NAMESPACES).text
    tripheadsign = self.__getservicedescription(xmlroot, txcserviceref)
    return Trip(tripid, serviceid, routeid, tripheadsign)

  def __getservicedescription(self, xmlroot, serviceref):
    for service in xmlroot.findall('txc:Services/txc:Service', self.TXC_NAMESPACES):
      if(service.find('txc:ServiceCode', self.TXC_NAMESPACES).text == serviceref):
        return service.find('txc:Description', self.TXC_NAMESPACES).text
    return null

  def __getvehiclejourneys(self, xmlroot):
    return xmlroot.findall('txc:VehicleJourneys/txc:VehicleJourney', self.TXC_NAMESPACES)

  def __writegtfstrips(self):
    print "- Writing trips.txt"
    with open('output/trips.txt', 'wb') as csvfile:
      csvwriter = csv.writer(csvfile)
      csvwriter.writerow(['trip_id', 'service_id', 'route_id', 'trip_headsign'])
      for route in self.trips:
        csvwriter.writerow(route.getgtfsvalues())
