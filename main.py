from extractors.AgencyExtractor import AgencyExtractor
from extractors.StopsDownloader import StopsDownloader

StopsDownloader().download()
AgencyExtractor().extract()
