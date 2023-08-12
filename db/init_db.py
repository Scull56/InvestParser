from utils.db_request import *

def init_db():
   db_request('invest_parser.db', '''
   CREATE TABLE IF NOT EXISTS companies (
      id INTEGER PRIMARY KEY,
      country TEXT DEFAULT "",
      industry TEXT DEFAULT "",
      sector TEXT DEFAULT "",
      title TEXT DEFAULT "",
      ebitda TEXT DEFAULT "",
      net_profit_margin TEXT DEFAULT "", 
      p_e TEXT DEFAULT "",
      p_s TEXT DEFAULT "", 
      diluted_eps TEXT DEFAULT "", 
      roe TEXT DEFAULT "", 
      roa TEXT DEFAULT "", 
      debt_to_equity TEXT DEFAULT "", 
      tech_analysis TEXT DEFAULT ""
   )
   ''')