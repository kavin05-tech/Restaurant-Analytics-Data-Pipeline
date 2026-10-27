import csv, logging, os, sys
from pathlib import Path
import psycopg2
from psycopg2.extras import execute_values
logging.basicConfig(level=os.getenv('LOG_LEVEL','INFO'), format='%(asctime)s %(levelname)s %(name)s %(message)s')
log=logging.getLogger('zomato_ingestion')
DATA=Path(os.getenv('ZOMATO_DATA_DIR', Path(__file__).resolve().parents[1]/'data'))
TABLES={
 'restaurants':(['restaurant_id','name','city','cuisine','rating','average_cost_for_two','online_order'],'restaurant_id',['int','str','str','str','float','int','str']),
 'orders':(['order_id','customer_id','restaurant_id','order_date','order_amount','status'],'order_id',['int','int','int','date','float','str']),
 'reviews':(['review_id','customer_id','restaurant_id','order_id','rating','review_text','review_date'],'review_id',['int','int','int','int','int','str','date'])}
DDL='''CREATE SCHEMA IF NOT EXISTS raw;
CREATE TABLE IF NOT EXISTS raw.restaurants (restaurant_id integer PRIMARY KEY, name text NOT NULL, city text NOT NULL, cuisine text, rating numeric(2,1), average_cost_for_two integer, online_order text);
CREATE TABLE IF NOT EXISTS raw.orders (order_id integer PRIMARY KEY, customer_id integer NOT NULL, restaurant_id integer NOT NULL, order_date date NOT NULL, order_amount numeric(10,2) NOT NULL, status text NOT NULL);
CREATE TABLE IF NOT EXISTS raw.reviews (review_id integer PRIMARY KEY, customer_id integer NOT NULL, restaurant_id integer NOT NULL, order_id integer NOT NULL, rating integer NOT NULL, review_text text, review_date date NOT NULL);'''
def convert(v,t):
 if t=='int': return int(v)
 if t=='float': return float(v)
 return v.strip()
def main():
 conn=psycopg2.connect(host=os.getenv('ZOMATO_DB_HOST','localhost'),port=os.getenv('ZOMATO_DB_PORT','5432'),dbname=os.getenv('ZOMATO_DB_NAME','zomato'),user=os.getenv('ZOMATO_DB_USER','zomato'),password=os.getenv('ZOMATO_DB_PASSWORD',''),connect_timeout=10)
 try:
  with conn:
   with conn.cursor() as cur:
    cur.execute(DDL)
    for table,(cols,key,types) in TABLES.items():
     path=DATA/f'{table}.csv'
     if not path.is_file(): raise FileNotFoundError(f'Missing source file: {path}')
     with path.open(newline='',encoding='utf-8-sig') as f:
      reader=csv.DictReader(f)
      if reader.fieldnames != cols: raise ValueError(f'{path.name} columns must be {cols}; got {reader.fieldnames}')
      rows=[tuple(convert(row[c],t) for c,t in zip(cols,types)) for row in reader]
     if not rows: raise ValueError(f'{path.name} has no records')
     update=','.join(f'{c}=EXCLUDED.{c}' for c in cols if c!=key)
     sql=f"INSERT INTO raw.{table} ({','.join(cols)}) VALUES %s ON CONFLICT ({key}) DO UPDATE SET {update}"
     execute_values(cur,sql,rows,page_size=1000)
     log.info('Upserted %d rows into raw.%s',len(rows),table)
  log.info('CSV ingestion completed')
 except Exception:
  conn.rollback(); log.exception('Ingestion transaction rolled back'); raise
 finally: conn.close()
if __name__=='__main__':
 try: main()
 except Exception: sys.exit(1)
