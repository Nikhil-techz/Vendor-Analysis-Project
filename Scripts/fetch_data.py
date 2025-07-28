import pandas as pd

from sqlalchemy import create_engine ,text
from config import get_engine
from analysis import  get_cleaned_vendor_summary


engine = get_engine() 


vendor_summary_table = get_cleaned_vendor_summary()


vendor_summary_table.to_sql(name='vendor_sales_summary',con=engine,if_exists='append',index=False)
print("data is inserted in table.") 


df = pd.read_sql(text("select * from vendor_sales_summary"),con=engine) 
print("fetched data:",df) 




