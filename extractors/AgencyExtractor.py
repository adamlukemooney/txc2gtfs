import csv
import xml.etree.ElementTree
import os
import sys

from models.Agency import Agency

class AgencyExtractor:
  PRINT_PROGRESS_INTERVAL = 0.1
  TXC_NAMESPACES = {'txc': 'http://www.transxchange.org.uk/'}

  inputfiles = os.listdir('input')
  totalfiles = len(inputfiles)
  progress = 0.0

  def extract(self):
    print "Extracting agencies from input directory"
    agencies = self.__extractagencies()
    self.__writegtfsagencies(agencies)
    print "- Done"

  def __extractagencies(self):
    sys.stdout.write('- Reading operators to agencies in memory')
    sys.stdout.flush()
    agencies = set()
    for index, file in enumerate(self.inputfiles):
      self.__printprogress(index)
      if file.endswith('.xml'):
        self.__process(file, agencies)
    print "."
    return agencies

  def __printprogress(self, currentindex):
    if(currentindex / float(self.totalfiles) > self.progress + self.PRINT_PROGRESS_INTERVAL):
      sys.stdout.write('.')
      sys.stdout.flush()
      self.progress += 0.1

  def __process(self, file, agencies):
    for operator in self.__getoperators(file):
      agencies.add(self.__convertoperatortoagency(operator))

  def __convertoperatortoagency(self, operator):
    agencyid = operator.attrib['id']
    agencyname = operator.find('txc:OperatorNameOnLicence', self.TXC_NAMESPACES).text
    agencyurl = 'https://www.google.com/#q=' + agencyname
    agencytimezone = 'Europe/London'
    return Agency(agencyid, agencyname, agencyurl, agencytimezone)

  def __getoperators(self, file):
    root = xml.etree.ElementTree.parse('input/' + file).getroot()
    return root.findall('txc:Operators/txc:Operator', self.TXC_NAMESPACES)

  def __writegtfsagencies(self, agencies):
    print "- Writing agencies.txt"
    with open('output/agency.txt', 'wb') as csvfile:
      csvwriter = csv.writer(csvfile)
      csvwriter.writerow(['agency_id', 'agency_name', 'agency_url', 'agency_timezone'])
      for agency in agencies:
        csvwriter.writerow(agency.getgtfsvalues())
