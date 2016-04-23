import csv
import xml.etree.ElementTree
import os
import sys

from models.StopTime import StopTime

class StopTimesExtractor:
  HOUR_IN_SECONDS = 60*60
  MINUTE_IN_SECONDS = 60
  PRINT_PROGRESS_INTERVAL = 0.1
  TXC_NAMESPACES = {'txc': 'http://www.transxchange.org.uk/'}

  csvwriter = None
  inputfiles = os.listdir('input')
  totalfiles = len(inputfiles)
  progress = 0.0

  def extract(self):
    print "Extracting stop times from input directory"
    with open('output/stop_times.txt', 'wb') as csvfile:
      self.csvwriter = csv.writer(csvfile)
      self.csvwriter.writerow(['trip_id', 'arrival_time', 'departure_time', 'stop_id', 'stop_sequence'])
      self.__extractstoptimes()
    print "- Done"

  def __extractstoptimes(self):
    sys.stdout.write('- Reading TXC JourneyPatternTimingLinks to GTFS stop times in stop_times.txt')
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
      self.__processvehiclejourney(vehiclejourney, xmlroot)

  def __getvehiclejourneys(self, xmlroot):
    return xmlroot.findall('txc:VehicleJourneys/txc:VehicleJourney', self.TXC_NAMESPACES)

  def __processvehiclejourney(self, vehiclejourney, xmlroot):
    tripid = vehiclejourney.find('txc:VehicleJourneyCode', self.TXC_NAMESPACES).text
    stopsequence = 0
    currenttime = self.__parsetime(vehiclejourney.find('txc:DepartureTime', self.TXC_NAMESPACES).text)
    links = self.__gettiminglinksforvehiclejourney(vehiclejourney, xmlroot)
    # All stops except last
    for link in links:
      runtime = self.__parseruntime(link.find('txc:RunTime', self.TXC_NAMESPACES).text)
      stopid = link.find('txc:From/txc:StopPointRef', self.TXC_NAMESPACES).text
      stopsequence = link.find('txc:From', self.TXC_NAMESPACES).attrib.get('SequenceNumber', str(int(stopsequence) + 1))
      outputtime = self.__secondstogtfstime(currenttime)
      self.csvwriter.writerow(StopTime(tripid, outputtime, outputtime, stopid, stopsequence).getgtfsvalues())
      currenttime = currenttime + runtime
    # Last stop
    stopid = links[-1].find('txc:To/txc:StopPointRef', self.TXC_NAMESPACES).text
    stopsequence = links[-1].find('txc:To', self.TXC_NAMESPACES).attrib.get('SequenceNumber', str(int(stopsequence) + 1))
    outputtime = self.__secondstogtfstime(currenttime)
    self.csvwriter.writerow(StopTime(tripid, outputtime, outputtime, stopid, stopsequence).getgtfsvalues())

  def __parsetime(self, timestring):
    split = timestring.split(":")
    return int(split[0]) * self.HOUR_IN_SECONDS + int(split[1]) * self.MINUTE_IN_SECONDS + int(split[2])

  def __gettiminglinksforvehiclejourney(self, vehiclejourney, xmlroot):
    journeypatternref = vehiclejourney.find('txc:JourneyPatternRef', self.TXC_NAMESPACES).text
    for journeypattern in self.__getalljourneypatterns(xmlroot):
      if journeypattern.attrib["id"] == journeypatternref:
        journeypatternsectionref = journeypattern.find('txc:JourneyPatternSectionRefs', self.TXC_NAMESPACES).text
        for journeypatternsection in self.__getalljourneypatternsections(xmlroot):
          if journeypatternsection.attrib["id"] == journeypatternsectionref:
            return journeypatternsection.findall('txc:JourneyPatternTimingLink', self.TXC_NAMESPACES)
    return []

  def __getalljourneypatterns(self, xmlroot):
    return xmlroot.findall('txc:Services/txc:Service/txc:StandardService/txc:JourneyPattern', self.TXC_NAMESPACES)

  def __getalljourneypatternsections(self, xmlroot):
    return xmlroot.findall('txc:JourneyPatternSections/txc:JourneyPatternSection', self.TXC_NAMESPACES)

  def __parseruntime(self, runtime):
    time = 0
    runtime = runtime.split("PT")[1]
    if 'H' in runtime:
      split = runtime.split("H")
      time = time + int(split[0]) * self.HOUR_IN_SECONDS
      runtime = split[1]
    if 'M' in runtime:
      split = runtime.split("M")
      time = time + int(split[0]) * self.MINUTE_IN_SECONDS
      runtime = split[1]
    if 'S' in runtime:
      split = runtime.split("S")
      time = time + int(split[0]) * self.MINUTE_IN_SECONDS
    return time

  def __secondstogtfstime(self, seconds):
    hours = seconds / self.HOUR_IN_SECONDS
    seconds = seconds - hours * self.HOUR_IN_SECONDS
    mins = seconds / self.MINUTE_IN_SECONDS
    seconds = seconds - mins * self.MINUTE_IN_SECONDS
    minpadding = "0" if mins < 10 else ""
    secpadding = "0" if seconds < 10 else ""
    return str(hours) + ":" + minpadding + str(mins) + ":" + secpadding + str(seconds)
