class Agency:
  def __init__(self, id, name, url, timezone):
    self.id = id
    self.name = name
    self.url = url
    self.timezone = timezone

  def __eq__(self, other):
    return self.id == other.getid() and self.name == other.getname() and self.url == other.geturl() and self.timezone == other.gettimezone()

  def __hash__(self):
    return hash(self.id)

  def getid(self):
    return self.id

  def getname(self):
    return self.name

  def geturl(self):
    return self.url

  def gettimezone(self):
    return self.timezone

  def getgtfsvalues(self):
    return [self.id, self.name, self.url, self.timezone]
