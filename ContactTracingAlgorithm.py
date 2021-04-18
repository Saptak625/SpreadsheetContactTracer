import datetime
from dbFunctions import queryContactTraceEntry, findAdjacentDesks, getContactedEntries

class CovidExposure():
  numOfIterations = None
  def __init__(self, name, startDate, iteration=0):
    self.name = name
    self.iteration = iteration
    self.startDate = startDate
    self.subCases = []
    if iteration <= numOfIterations:
      self.contactTrace()

  def contactTrace(self):
    #Query entries to find all locations.
    allInstances = queryContactTraceEntry()
    #For each location find all adjacent users
    for record in allInstances:
      adjacentDesks=findAdjacentDesks(record[2]+'_'+record[3])
      #Check if entry exists for according desks in oldEntries table given 30 range(back and forth)
      timeDelta = datetime.timedelta(minutes=15)
      startTime = record[-1] - timeDelta
      endTime = record[-1] + timeDelta
      for deskAssociation in adjacentDesks:
        physicalClassroom, desk = deskAssociation[1].split('_')
        contactedEntries = getContactedEntries(physicalClassroom, desk, startTime, endTime)
        for entry in contactedEntries:
          #Create new CovidExposure for each user and append to subCases
          self.subCases.append(CovidExposure(entry[1], entry[-1], iteration=self.iteration + 1))