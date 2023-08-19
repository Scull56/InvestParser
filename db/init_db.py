from utils.db_request import *

def init_db():
   db_request('invest_parser.db', '''
   CREATE TABLE IF NOT EXISTS companies (
      id INTEGER PRIMARY KEY,
      company_id INTEGER,
      url TEXT,
      country TEXT DEFAULT "",
      industry TEXT DEFAULT "",
      sector TEXT DEFAULT "",
      title TEXT,
      ebitda INTEGER,
      net_profit_margin REAL, 
      p_e REAL,
      p_s REAL,
      eps REAL,
      roe REAL, 
      roa REAL,
      debt_to_equity REAL,
      tech_analysis TEXT
   )
   ''')