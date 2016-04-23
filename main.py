from extractors.AgencyExtractor import AgencyExtractor
from extractors.RoutesExtractor import RoutesExtractor
from extractors.StopsDownloader import StopsDownloader
from extractors.StopTimesExtractor import StopTimesExtractor
from extractors.TripsExtractor import TripsExtractor

StopsDownloader().download()
AgencyExtractor().extract()
RoutesExtractor().extract()
TripsExtractor().extract()
StopTimesExtractor().extract()
