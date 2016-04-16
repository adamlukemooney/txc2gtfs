from extractors.AgencyExtractor import AgencyExtractor
from extractors.RoutesExtractor import RoutesExtractor
from extractors.StopsDownloader import StopsDownloader
from extractors.TripsExtractor import TripsExtractor

StopsDownloader().download()
AgencyExtractor().extract()
RouteExtractor().extract()
TripsExtractor().extract()