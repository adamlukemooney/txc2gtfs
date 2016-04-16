from extractors.AgencyExtractor import AgencyExtractor
from extractors.RouteExtractor import RouteExtractor
from extractors.StopsDownloader import StopsDownloader

StopsDownloader().download()
AgencyExtractor().extract()
RouteExtractor().extract()
