class Trip:
  def __init__(self, id, serviceid, routeid, tripheadsign):
    self.id = id
    self.serviceid = serviceid
    self.routeid = routeid
    self.tripheadsign = tripheadsign

  def __eq__(self, other):
    return self.id == other.getid()

  def __hash__(self):
    return hash(self.id)

  def getid(self):
    return self.id

  def getserviceid(self):
    return self.serviceid

  def getrouteid(self):
    return self.routeid

  def gettripheadsign(self):
    return self.tripheadsign

  def getgtfsvalues(self):
    return [self.id, self.serviceid, self.routeid, self.tripheadsign]
