import csv
import xml.etree.ElementTree
import os

from agency import Agency

txcnamespaces = {'txc': 'http://www.transxchange.org.uk/'}

def extractagencies():
  agencies = set()
  for file in os.listdir('input'):
    if file.endswith('.xml'):
      print 'Processing ' + file + '...'
      process(file, agencies)
  return agencies

def process(file, agencies):
  for operator in getoperators(file):
    agencies.add(convertoperatortoagency(operator))

def convertoperatortoagency(operator):
  agencyid = operator.attrib['id']
  agencyname = operator.find('txc:OperatorNameOnLicence', txcnamespaces).text
  agencyurl = 'https://www.google.com/#q=' + agencyname
  agencytimezone = 'Europe/London'
  return Agency(agencyid, agencyname, agencyurl, agencytimezone)

def getoperators(file):
  root = xml.etree.ElementTree.parse('input/' + file).getroot()
  return root.findall('txc:Operators/txc:Operator', txcnamespaces)

def writegtfsagencies(agencies):
  with open('output/agency.txt', 'wb') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['agency_id', 'agency_name', 'agency_url', 'agency_timezone'])
    for agency in agencies:
      csvwriter.writerow(agency.getgtfsvalues())

writegtfsagencies(extractagencies())