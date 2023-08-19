from utils.db_request import *

db_url = 'invest_parser.db'

def get_companies():
   
   command = "SELECT * FROM companies"
   
   return db_request(db_url, command)

def get_company_by_id(id):
   
   command = f"SELECT company_id FROM companies WHERE company_id = {id}"
   
   return db_request(db_url, command)

def get_last_company_id():
   
   command = "SELECT id FROM companies ORDER BY id DESC LIMIT 1"
   
   return db_request(db_url, command)

def add_company(data):
   
   values = f'"{data["company_id"]}", "{data["url"]}", "{data["country"]}", "{data["industry"]}", "{data["sector"]}", "{data["title"]}", "{data["ebitda"]}", "{data["net_profit_margin"]}", "{data["p_e"]}", "{data["p_s"]}", "{data["eps"]}", "{data["roe"]}", "{data["roa"]}", "{data["debt_to_equity"]}", "{data["tech_analysis"]}"'
   
   command = f"INSERT INTO companies (company_id, url, country, industry, sector, title, ebitda, net_profit_margin, p_e, p_s, eps, roe, roa, debt_to_equity, tech_analysis) VALUES ({values})"
   
   return db_request(db_url, command)

def get_countries():
   
   command = "SELECT DISTINCT country FROM companies"
   
   return db_request(db_url, command)
   
def get_industries():
   
   command = "SELECT DISTINCT industry FROM companies"
   
   return db_request(db_url, command)
   

def get_sectors():
   
   command = "SELECT DISTINCT sector FROM companies"
   
   return db_request(db_url, command)

def delete_companies(id_list):
   
   id_string = map(lambda id: f'id = {id}', id_list)
   id_string = ' OR '.join(id_string)
   
   command = f"DELETE FROM companies WHERE {id_string}"
   
   return db_request(db_url, command)
   
   