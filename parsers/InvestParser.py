import requests
from bs4 import BeautifulSoup as bs
import re

from utils.InvestExceptions import *

class InvestParser():
   
   def __init__(self, company):
      
      urlSummary = f'https://www.investing.com/equities/{company}-financial-summary'
      urlIncome = f'https://www.investing.com/equities/{company}-income-statement'
      urlRatios = f'https://www.investing.com/equities/{company}-ratios'
      urlTechnical = f'https://www.investing.com/equities/{company}-technical'
      urlProfile = f'https://www.investing.com/equities/{company}-company-profile'
      
      summary_res = requests.get(urlSummary)
      income_res = requests.get(urlIncome)
      ratios_res = requests.get(urlRatios)
      technical_res = requests.get(urlTechnical)
      profile_res = requests.get(urlProfile)
      
      if summary_res.status_code == 404:
         raise NotFoundCompany()
      
      if income_res.status_code == 404:
         raise NotFoundCompany()
      
      if ratios_res.status_code == 404:
         raise NotFoundCompany()
      
      if technical_res.status_code == 404:
         raise NotFoundCompany()
      
      if profile_res.status_code == 404:
         raise NotFoundCompany()
      
      self.summary = bs(summary_res.text, "html.parser")
      self.income =bs(income_res.text, "html.parser")
      self.ratios =  bs(ratios_res.text, "html.parser")
      self.technical = bs(technical_res.text, "html.parser")
      self.profile = bs(profile_res.text, "html.parser")
      
   def parse(self):
      
      result = {}
      
      result["country"] = self.parse_country()
      result["industry"] = self.parse_industry()
      result['sector'] = self.parse_sector()
      result["title"] = self.parse_title()
      result["ebitda"] = self.parse_ebitda()
      result["net_profit_margin"] = self.parse_from_summary('Net Profit margin')
      result["debt_to_equity"] = self.parse_from_summary('Total Debt to Equity')
      result["diluted_eps"] = self.parse_from_income('Diluted Normalized EPS')
      result["p_e"] = self.parse_from_ratios('P/E Ratio ')
      result["p_s"] = self.parse_from_ratios('Price to Sales ')
      result["roe"] = self.parse_from_ratios('Return on Equity ')
      result["roa"] = self.parse_from_ratios('Return on Assets ')
      result['tech_analysis'] = self.parse_tech_analysis()
      
      return result
   
   def parse_title(self):

      elem = self.summary.find('h1')
     
      if elem.string == None:
         return ""
     
      return re.sub(r'\) ', ')', elem.string)
      
   def parse_ebitda(self):
      
      summaryText = self.summary.find("p", id="profile-story")
      
      if summaryText == None:
         return ""
      
      summaryText = summaryText.string
      
      summaryText = re.search(r'was \D+\S+ [^\. ]*', summaryText)
            
      summaryText = re.sub(r'was ', '', summaryText[0])
      
      summaryText = re.split(' ', summaryText)
      
      summaryText[1] = float(re.sub(',', '.', summaryText[1]))
      
      if len(summaryText) == 3:
         if summaryText[2] == "million":
            return f'{summaryText[0]} {summaryText[1] / 1000}'
         if summaryText[2] == "billion":
            return f'{summaryText[0]} {summaryText[1]}'
      else:
         return ""
       
   def parse_from_summary(self, text):
      
      attrs = {
         "class": "float_lang_base_2 text_align_lang_base_2 dirLtr bold"
      }
      
      elem = self.summary.find('span', text=text)
      elem = elem.find_next_sibling(attrs=attrs)
      
      if elem == None:
         return ""
       
      return re.sub(' ', '', elem.string)
   
   def parse_from_income(self, text):
      
      elem = self.income.find(text=text)
      elem = elem.parent.parent.parent
      
      try:
         elem = elem.contents[3]
      except:
         return ""
      
      return elem.string
   
   def parse_from_ratios(self, text):
      
      elem = self.ratios.find(text=text)
      elem = elem.parent.parent.parent
      
      try:
         elem = elem.contents[3]
      except:
         return ""
      
      return elem.string
   
   def parse_tech_analysis(self):
      
      elem = self.technical.find(text='Summary:')
      elem = elem.next_sibling
      
      return elem.string
   
   def parse_country(self):
      
      elem = self.profile.find('span', text='Address')
      
      if elem == None:
         return ""
      
      elem = elem.next_element.next_element.next_element
      
      if elem == None:
         return ""
      
      elem = elem.contents[-1]

      return elem.string
   
   def parse_industry(self):
      
      attrs = {
         "class": "companyProfileHeader"
      }
      
      elem = self.profile.find("div", attrs=attrs)
      
      elem = elem.contents[1].a
   
      return elem.string
   
   def parse_sector(self):
      attrs = {
         "class": "companyProfileHeader"
      }
      
      elem = self.profile.find("div", attrs=attrs)
      
      elem = elem.contents[3].a
   
      return elem.string