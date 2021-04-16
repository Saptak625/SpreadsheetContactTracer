class CovidExposure():
  numOfIterations = None
  def __init__(self, name, startDate, iteration=0):
    self.name = name
    self.iteration = iteration
    self.startDate = startDate
    self.subCases = []
    if iteration <= numOfIterations:
      self.fetchContactedUsers()


  def fetchContactedUsers(self):
    #Query entries to find all locations.

    #For each location find all adjacent users
    #Create new CovidExposure for each user and append to subCases
    print('Needs to implemented later.')