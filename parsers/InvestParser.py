import requests
from parsel import Selector
import re

from utils.InvestExceptions import *

class InvestParser():
   
   def __init__(self, id, company):
      
      company = company.split('?')
      
      company_path = company[0]
      company_query = ''
      
      if len(company) > 1:
         company_query = company[1]
      
      urlSummary = f'https://www.investing.com/instruments/Financials/changesummaryreporttypeajax?action=change_report_type&pid={id}&financial_id={id}&ratios_id={id}&period_type=Annual'
      urlRatios = f'https://www.investing.com/{company_path}-ratios{"?" + company_query if company_query != "" else ""}'
      urlTechnical = f'https://www.investing.com/{company_path}/technical/technical-summary{"?" + company_query if company_query != "" else ""}'
      urlIncome = f'https://www.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID={id}&report_type=INC&period_type=Annual'
      
      summary_res = requests.get(urlSummary)
      ratios_res = requests.get(urlRatios)
      technical_res = requests.get(urlTechnical)
      income_res = requests.get(urlIncome)
      
      if summary_res.status_code != 200:
         raise NotFoundCompany()
      
      if ratios_res.status_code != 200:
         raise NotFoundCompany()
      
      if technical_res.status_code != 200:
         raise NotFoundCompany()
      
      if income_res.status_code != 200:
         raise NotFoundCompany()
      
      self.summary = Selector(text=summary_res.text)
      self.ratios =  Selector(text=ratios_res.text)
      self.technical = Selector(text=technical_res.text)
      self.income = Selector(text=income_res.text)
      
   def parse(self):
      
      result = {}
      errors = []
      
      result["country"] = self.parse_country()
      result["industry"] = self.parse_info('Industry')
      result['sector'] = self.parse_info('Sector')
      result["title"] = self.parse_title()
      result["ebitda"] = self.parse_ebitda()
      result["net_profit_margin"] = self.parse_net_profit_margin()
      result["debt_to_equity"] = self.parse_debt_to_equity()
      result["eps"] = self.parse_eps()
      result["p_e"] = self.parse_p_e()
      result["p_s"] = self.parse_from_ratios('Price to Sales ')
      result["roe"] = self.parse_roe()
      result["roa"] = self.parse_roa()
      result['tech_analysis'] = self.parse_tech_analysis()
      
      for param in result.keys():
         
         if result[param] == None:
            
            errors.append(param)
      
      if len(errors) > 0:
         
         raise NotFoundParams(errors)
      
      float_list = ['ebitda', 'net_profit_margin', 'debt_to_equity', 'eps', 'p_e', 'p_s', 'roe', 'roa']

      for name in float_list:

         result[name] = float(result[name])
      
      return result
   
   def parse_title(self):
     
      title = self.ratios.xpath('//h1/text()').get()
      
      if title == None:
         return None
      
      return re.sub(r'\) ', ')', title)
      
   def parse_ebitda(self):
      
      ebitda = self.summary.xpath("/html/body/div[1]/table/tbody/tr[1]/td[2]/text()").get()
      
      if ebitda == None:
         ebitda = self.summary.xpath("/html/body/div[1]/table/tbody/tr[1]/td[3]/text()").get()
      
      return ebitda
   
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
      
      value = round((float(debt) / float(equity)), 2)
         
      return value
   
   def parse_net_profit_margin(self):
      
      npm = self.parse_from_ratios('Net Profit margin ')
      
      if npm == None:
         income = self.parse_net_income()
         ebitda = self.parse_ebitda()
         
         if income == None or ebitda == None:
            return None
         
         npm = round((float(income) / float(ebitda)), 2)
         
      else:
         npm = float(re.sub(r'%', '', npm)) / 100
         
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
         
         roa = round((float(income) / float(assets)), 2)
         
      else:
         roa = float(re.sub(r'%', '', roa)) / 100
         
      return roa
   
   def parse_roe(self):
      
      roe = self.parse_from_ratios('Return on Equity ')
      
      if roe == None or roe == '0%':
         income = self.parse_net_income()
         equity = self.parse_equity()
         
         if income == None or equity == None:
            return None
         
         roe = round((float(income) / float(equity)), 2)
      else:
         roe = float(re.sub(r'%', '', roe)) / 100
         
      return roe
   
   def parse_p_e(self):
      
      p_e = self.parse_from_ratios('P/E Ratio ')
      
      if p_e == None:
         p_e = self.parse_from_technical('P/E Ratio')
         
      return p_e
   
   def parse_eps(self):
         
      eps = self.parse_from_technical('EPS')
      
      if eps == None:
         eps = self.parse_from_ratios('Basic EPS ')
      
      if eps == None:
         eps = self.parse_from_ratios('Diluted EPS ')
      
      if eps == None:
         eps = self.income.xpath('//span[text()="Diluted Normalized EPS"]/../following-sibling::td[1]/text()').get()
      
      if eps == None:
         eps = self.income.xpath('//span[text()="Diluted Normalized EPS"]/../following-sibling::td[2]/text()').get()
         
      return eps
   
   def parse_from_ratios(self, text):
      
      ratio = self.ratios.xpath(f'//table[@id="rrTable"]//span[text()="{text}"]/../following-sibling::td[1]/text()').get()
      
      if ratio == '-':
         return None
      
      return ratio
   
   def parse_tech_analysis(self):
      
      return self.technical.xpath('//table/tbody/tr[3]/td[6]/text()').get()
   
   def parse_from_technical(self, text):
      
      return self.technical.xpath(f'//dt[text()="{text}"]/following-sibling::dd/span/span[2]/text()').get()
   
   def parse_country(self):
      
      country = self.parse_info('Market')
      
      if country == None:
         country = self.ratios.xpath(f'//span[text()="Market:"]/following-sibling::span/@title').get()
   
      return country
   
   def parse_info(self, text):
      
      info = self.technical.xpath(f'//div[text()="{text}"]/following-sibling::a[1]/text()').get()
      
      if info == None:
         info = self.technical.xpath(f'//div[text()="{text}"]/a/text()').get()
         
      return info