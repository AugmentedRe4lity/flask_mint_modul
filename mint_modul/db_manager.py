import sqlite3

def init_db(dat):
  try:
    with sqlite3.connect('data.db') as conn:
      datestring = dat.replace('.','')
      conn.execute(f'CREATE TABLE daten{datestring} (Uhrzeit TIME, Ort VARCHAR(3), Temperatur INTEGER, Nitrat INTEGER, NitratWINLAB NUMERIC(10, 5), Nitrit NUMERIC(10, 5), Ammonium NUMERIC(10,5), AmmoniumWINLAB NUMERIC(10,5), Phosphat NUMERIC(10,5), PhosphatWINLAB NUMERIC(10,5), pHWert NUMERIC(3,1), GPSLaengengrad NUMERIC(20,10), GPSBreitengrad NUMERIC(20,10))')
    return True
  except:
    return False
    

def add_to_db(arguments):
  dat = arguments[0]
  dat = dat.replace('.', '')
  with sqlite3.connect('data.db') as conn:
    cursor = conn.cursor()
    cursor.execute(f'INSERT INTO daten{dat} VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)', (arguments[1],arguments[2],arguments[3],arguments[4],arguments[5],arguments[6],arguments[7],arguments[8],arguments[9],arguments[10],arguments[11],arguments[12],arguments[13]))
    conn.commit()

def get_db_data(dat):
  with sqlite3.connect('data.db') as conn:
    cursor = conn.cursor()
    dat = dat.replace('.','')
    cursor.execute(f'SELECT * FROM daten{dat}')
    rows = cursor.fetchall()
  return rows

def get_db_tables():
  with sqlite3.connect('data.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
  return tables