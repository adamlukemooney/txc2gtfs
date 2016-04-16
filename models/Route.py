class Route:
  def __init__(self, id, agencyid, name, type):
    self.id = id
    self.agencyid = agencyid
    self.name = name
    self.type = type

  def __eq__(self, other):
    return self.id == other.getid()

  def __hash__(self):
    return hash(self.id)

  def getid(self):
    return self.id

  def getagencyid(self):
    return self.agencyid

  def getlongname(self):
    return self.name

  def getshortname(self):
    return self.name

  def gettype(self):
    return self.type

  def getgtfsvalues(self):
    return [self.id, self.agencyid, self.name, self.name, self.type]
