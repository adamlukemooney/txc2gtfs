import csv
import xml.etree.ElementTree
import os

from models.Agency import Agency

class AgencyExtractor:
  TXC_NAMESPACES = {'txc': 'http://www.transxchange.org.uk/'}

  def extract(self):
    agencies = self.__extractagencies()
    self.__writegtfsagencies(agencies)

  def __extractagencies(self):
    agencies = set()
    for file in os.listdir('input'):
      if file.endswith('.xml'):
        print 'Processing ' + file + '...'
        self.__process(file, agencies)
    return agencies

  def __process(self, file, agencies):
    for operator in self.__getoperators(file):
      agencies.add(self.__convertoperatortoagency(operator))

  def __convertoperatortoagency(self, operator):
    agencyid = operator.attrib['id']
    agencyname = operator.find('txc:OperatorNameOnLicence', AgencyExtractor.TXC_NAMESPACES).text
    agencyurl = 'https://www.google.com/#q=' + agencyname
    agencytimezone = 'Europe/London'
    return Agency(agencyid, agencyname, agencyurl, agencytimezone)

  def __getoperators(self, file):
    root = xml.etree.ElementTree.parse('input/' + file).getroot()
    return root.findall('txc:Operators/txc:Operator', AgencyExtractor.TXC_NAMESPACES)

  def __writegtfsagencies(self, agencies):
    with open('output/agency.txt', 'wb') as csvfile:
      csvwriter = csv.writer(csvfile)
      csvwriter.writerow(['agency_id', 'agency_name', 'agency_url', 'agency_timezone'])
      for agency in agencies:
        csvwriter.writerow(agency.getgtfsvalues())
