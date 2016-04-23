class StopTime:
  def __init__(self, tripid, arrivaltime, departuretime, stopid, stopsequence):
    self.tripid = tripid
    self.arrivaltime = arrivaltime
    self.departuretime = departuretime
    self.stopid = stopid
    self.stopsequence = stopsequence

  def __eq__(self, other):
    return self.id == other.getid()

  def __hash__(self):
    return hash(self.id)

  def gettripid(self):
    return self.tripid

  def getarrivaltime(self):
    return self.arrivaltime

  def getdeparturetime(self):
    return self.departuretime

  def getstopid(self):
    return self.stopid

  def getstopsequence(self):
    return self.stopsequence

  def getgtfsvalues(self):
    return [self.tripid, self.arrivaltime, self.departuretime, self.stopid, self.stopsequence]
