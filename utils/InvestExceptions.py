class NotFoundCompany(Exception):
   pass

class NotFoundParams(Exception):
   def __init__(self, params):
      super().__init__()
      self.params = params
      
class NotFoundCompanyParams(Exception):
   def __init__(self, companies):
         super().__init__()
         self.companies = companies
class CompanyAlreadyAdded(Exception):
   pass