import datetime
from dbFunctions import queryContactTraceEntry, findAdjacentDesks, getContactedEntries

class CovidExposure():
  numOfIterations = None
  def __init__(self, name, startDate, iteration=0, parents = []):
    self.name = name
    self.iteration = iteration
    self.startDate = startDate
    self.subCases = []
    self.parents = parents
    if iteration <= CovidExposure.numOfIterations:
      self.contactTrace()

  def contactTrace(self):
    #Query entries to find all locations.
    allInstances = queryContactTraceEntry(self.name, self.startDate)
    #For each location find all adjacent users
    for record in allInstances:
      adjacentDesks=findAdjacentDesks(record[2]+'_'+record[3])
      #Check if entry exists for according desks in oldEntries table given 30 range(back and forth)
      timeDelta = datetime.timedelta(minutes=15)
      startTime = record[-1] - timeDelta
      endTme = record[-1] + timeDelta
      for deskAssociation in adjacentDesks:
        physicalClassroom, desk = deskAssociation[1].split('_')
        contactedEntries = getContactedEntries(physicalClassroom, desk, startTime, endTime)
        for entry in contactedEntries:
          #Check if current entry called tree(check if in parent)
          if not self.checkIfParent(entry):
            #Create new CovidExposure for each user and append to subCases
            self.subCases.append(CovidExposure(entry[1], entry[-1], iteration=self.iteration + 1), parents=self.parents+[self])

  def checkIfParent(self, entry):
    for parent in self.parents:
      if self.name == entry[1]:
        #Parent found
        return True
    return False

  def parseResultsInto1DList(self):
    flattenedList = [self]
    for child in self.subCases:
      flattenedList += child.parseResultsInto1DList()
    del flattenedList[0]
    def sortByIterations(e):
      return e.iteration
    flattenedList.sort(key=sortByIterations)
    return flattenedList 