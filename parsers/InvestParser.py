import requests
from parsel import Selector
import re

from utils.InvestExceptions import *

class InvestParser():
   
   def __init__(self, id, company):
      
      urlSummary = f'https://www.investing.com/instruments/Financials/changesummaryreporttypeajax?action=change_report_type&pid={id}&financial_id={id}&ratios_id={id}&period_type=Annual'
      urlRatios = f'https://www.investing.com/{company}-ratios'
      urlTechnical = f'https://www.investing.com/{company}/technical/technical-summary'
      
      summary_res = requests.get(urlSummary)
      ratios_res = requests.get(urlRatios)
      technical_res = requests.get(urlTechnical)
      
      if summary_res.status_code == 404:
         raise NotFoundCompany()
      
      if ratios_res.status_code == 404:
         raise NotFoundCompany()
      
      if technical_res.status_code == 404:
         raise NotFoundCompany()
      
      self.summary = Selector(text=summary_res.text)
      self.ratios =  Selector(text=ratios_res.text)
      self.technical = Selector(text=technical_res.text)
      
   def parse(self):
      
      result = {}
      errors = []
      
      result["country"] = self.parse_info('Market')
      result["industry"] = self.parse_info('Industry')
      result['sector'] = self.parse_info('Sector')
      result["title"] = self.parse_title()
      result["ebitda"] = self.parse_ebitda()
      result["net_profit_margin"] = self.parse_net_profit_margin()
      result["debt_to_equity"] = self.parse_debt_to_equity()
      result["eps"] = self.parse_from_ratios('Basic EPS ')
      result["p_e"] = self.parse_from_ratios('P/E Ratio ')
      result["p_s"] = self.parse_from_ratios('Price to Sales ')
      result["roe"] = self.parse_roe()
      result["roa"] = self.parse_roa()
      result['tech_analysis'] = self.parse_tech_analysis()
      
      for param in result.keys():
         
         if result[param] == None:
            
            errors.append(param)
      
      if len(errors) > 0:
         
         raise NotFoundParams(errors)
      
      return result
   
   def parse_title(self):
     
      title = self.ratios.xpath('//h1/text()').get()
      
      if title == None:
         return None
      
      return re.sub(r'\) ', ')', title)
      
   def parse_ebitda(self):
      
      return self.summary.xpath("/html/body/div[1]/table/tbody/tr[1]/td[2]/text()").get()
   
   def parse_net_income(self):
      
      income = self.summary.xpath("/html/body/div[1]/table/tbody/tr[4]/td[2]/text()").get()
      
      if income == None:
         income = self.summary.xpath("/html/body/div[1]/table/tbody/tr[4]/td[3]/text()").get()
   
      return income
   
   def parse_equity(self):
      equity = self.summary.xpath('//td[text()="Total Equity"]/following-sibling::td[1]/text()').get()
      
      if equity == None:
         equity = self.summary.xpath('//td[text()="Total Equity"]/following-sibling::td[2]/text()').get()
         
      return equity
   
   def parse_debt_to_equity(self):
      
      equity = self.parse_equity()
      debt = self.summary.xpath('//td[text()="Total Liabilities"]/following-sibling::td[1]/text()').get()
      
      if equity == None or debt == None:
         return None
      
      value = round((int(debt) / int(equity)) * 100, 2)
         
      return value
   
   def parse_net_profit_margin(self):
      
      npm = self.parse_from_ratios('Net Profit margin ')
      
      if npm == None:
         income = self.parse_net_income()
         ebitda = self.parse_ebitda()
         
         if income == None or ebitda == None:
            return None
         
         npm = round((int(income) / int(ebitda)) * 100, 2)
         
      else:
         npm = re.sub(r'%', '', npm)
         
      return npm
   
   def parse_assets(self):
      assets = self.summary.xpath("/html/body/div[3]/table/tbody/tr[1]/td[2]/text()").get()

      if assets == None:
         assets = self.summary.xpath("/html/body/div[3]/table/tbody/tr[1]/td[3]/text()").get()
         
      return assets
   
   def parse_roa(self):
      roa = self.parse_from_ratios('Return on Assets ')
      
      if roa == None or roa == '0%':
         income = self.parse_net_income()
         assets = self.parse_assets()
         
         if income == None or assets == None:
            return None
         
         roa = round((int(income) / int(assets)) * 100, 2)
         
      else:
         roa = re.sub(r'%', '', roa)
         
      return roa
   
   def parse_roe(self):
      roe = self.parse_from_ratios('Return on Equity ')
      
      if roe == None or roe == '0%':
         income = self.parse_net_income()
         equity = self.parse_equity()
         
         if income == None or equity == None:
            return None
         
         roe = round((int(income) / int(equity)) * 100, 2)
      else:
         roe = re.sub(r'%', '', roe)
         
      return roe
   
   def parse_from_ratios(self, text):
      
      return self.ratios.xpath(f'//table[@id="rrTable"]//span[text()="{text}"]/../following-sibling::td[1]/text()').get()
   
   def parse_tech_analysis(self):
      
      return self.technical.xpath('//table/tbody/tr[3]/td[6]/text()').get()
   
   def parse_info(self, text):
      
      return self.technical.xpath(f'//div[text()="{text}"]/following-sibling::a[1]/text()').get()