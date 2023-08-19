class NotFoundCompany(Exception):
   pass

class NotFoundParams(Exception):
   def __init__(self, params):
      super().__init__()
      self.params = params

class CompanyAlreadyAdded(Exception):
   pass