import pandas as pd
from sqlalchemy import inspect, text
from config import get_engine

engine = get_engine()

with engine.connect() as conn: 
     inspector = inspect(engine)
     tables = inspector.get_table_names()
     print("Tables present in database:", tables) 
    









##to see the data in each table . 
    
     for table in tables:
        query = text(f"select * from `{table}` limit 5")
        df = pd.read_sql(query,conn)
        print(f"{table} (first 5 rows)---")
        print(df) 

     query = text(f"select * from Purchases WHERE  vendornumber = 4466")
     df= pd.read_sql(query,conn)
     print(df) 







        
