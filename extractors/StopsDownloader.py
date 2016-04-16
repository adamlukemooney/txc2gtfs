import urllib
import os
import zipfile
import errno

class StopsDownloader:
  TEMP_DIR = "tmp"
  NAPTAN_GTFS_DOWNLOAD_URL = "http://www.dft.gov.uk/NaPTAN/snapshot/GTFS.zip"
  LOCAL_ZIP_DESTINATION = "tmp/naptan.zip"

  def download(self):
    print "Downloading stops from NaPTAN database"
    self.__preparetempdirectory()
    self.__downloadzipfile()
    self.__extractzipfile()
    print "- Done"

  def __preparetempdirectory(self):
    print "- Preparing temp directory"
    try:
      os.makedirs(self.TEMP_DIR)
    except OSError as exception:
      if exception.errno != errno.EEXIST:
        raise

  def __downloadzipfile(self):
    print "- Downloading ZIP file to temp directory"
    urllib.urlretrieve (self.NAPTAN_GTFS_DOWNLOAD_URL, self.LOCAL_ZIP_DESTINATION)

  def __extractzipfile(self):
    print "- Extracting stops.txt from ZIP"
    with zipfile.ZipFile(self.LOCAL_ZIP_DESTINATION, "r") as z:
      z.extractall("output/")