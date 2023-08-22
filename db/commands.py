from utils.db_request import *

import sqlite3 as sq
import aiosqlite

db_url = 'data/invest_parser.db'

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

def get_info():
   
   result = {}
   
   connect = sq.connect(db_url)
   cursor = connect.cursor()
   
   country = "SELECT DISTINCT country FROM companies"
   sector = "SELECT DISTINCT sector FROM companies"
   industry = "SELECT DISTINCT industry FROM companies"
   
   cursor.execute(country)
   
   result['country'] = cursor.fetchall()
   
   cursor.execute(sector)
   
   result['sector'] = cursor.fetchall()
   
   cursor.execute(industry)
   
   result['industry'] = cursor.fetchall()
   
   connect.commit()
   
   return result

def delete_companies(id_list):
   
   id_string = map(lambda id: f'id = {id}', id_list)
   id_string = ' OR '.join(id_string)
   
   command = f"DELETE FROM companies WHERE {id_string}"
   
   return db_request(db_url, command)

def get_companies_info():
   
   command = 'SELECT id, company_id, url, title FROM companies'
   
   return db_request(db_url, command)

async def update_companies(data_list):
   
   db = await aiosqlite.connect(db_url)
   
   for data in data_list:
      
      id = data["id"]
      c = data["country"]
      s = data["sector"]
      i = data["industry"]
      e = data["ebitda"]
      n = data["net_profit_margin"]
      pe = data["p_e"] 
      ps = data["p_s"]
      ep = data["eps"]
      oe = data["roe"]
      oa = data["roa"]
      de = data["debt_to_equity"]
      t = data["tech_analysis"]
      
      cursor = await db.execute(f'UPDATE companies SET country = "{c}", sector = "{s}", industry = "{i}", ebitda = {e}, net_profit_margin = {n}, p_e = {pe}, p_s = {ps}, eps = {ep}, roe = {oe}, roa = {oa}, debt_to_equity = {de}, tech_analysis = "{t}" WHERE id = {id}')
      
      await cursor.close()
   
   await db.close()
   