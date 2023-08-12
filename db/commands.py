from utils.db_request import *

def get_companies():
   
   command = "SELECT * FROM companies"
   
   return db_request('invest_parser.db', command)

def add_company(data):
   
   values = f'"{data["country"]}", "{data["industry"]}", "{data["sector"]}", "{data["title"]}", "{data["ebitda"]}", "{data["net_profit_margin"]}", "{data["p_e"]}", "{data["p_s"]}", "{data["diluted_eps"]}", "{data["roe"]}", "{data["roa"]}", "{data["debt_to_equity"]}", "{data["tech_analysis"]}"'
   
   command = f"INSERT INTO companies (country, industry, sector, title, ebitda, net_profit_margin, p_e, p_s, diluted_eps, roe, roa, debt_to_equity, tech_analysis) VALUES ({values})"
   
   return db_request('invest_parser.db', command)

def get_countries():
   
   command = "SELECT DISTINCT country FROM companies"
   
   return db_request('invest_parser.db', command)
   
def get_industries():
   
   command = "SELECT DISTINCT industry FROM companies"
   
   return db_request('invest_parser.db', command)
   

def get_sectors():
   
   command = "SELECT DISTINCT sector FROM companies"
   
   return db_request('invest_parser.db', command)
   