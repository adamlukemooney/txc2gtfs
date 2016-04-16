mapping = {
  "air": 1100,
  "bus": 3,
  "coach": 3,
  "ferry": 4,
  "metro": 1,
  "rail": 2,
  "tram": 0,
  "trolleyBus": 3,
  "underground": 1
}

def txcmodetogtfstype(mode):
  if(mode in mapping):
    return mapping[mode]
  else:
    raise LookupError("Unexpected transport mode encountered: " + mode)