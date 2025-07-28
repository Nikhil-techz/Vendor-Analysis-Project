import pandas as pd
import logging
import os
from config import get_engine 
engine = get_engine()

##logging setup ## 

logging.basicConfig(
    filename='E:/VENDOR PROJECT/Logs/vendors_import.log',
    level=logging.INFO,
    format='%(asctime)s- %(levelname)s- %(message)s'
)

files = { 
    "begin_inventory": "E:/Vendor Project/Data/begin_inventory.csv",
    "end_inventory": "E:/Vendor Project/Data/End_inventory.csv",
    "purchase_price": "E:/Vendor Project/Data/Purchase_prices.csv",
    "sale": "E:/Vendor Project/Data/sale.csv",
    "vendor_invoice": "E:/Vendor Project/Data/vendor_invoice.csv",
    "purchases": "E:/Vendor Project/Data/Purchases.csv"

}

for table , path in files.items():
    if os.path.exists(path):
        df = pd.read_csv(path,low_memory=False)
        logging.info(f"[DEBUG] Table: {table}, Rows: {len(df)}, Columns: {list(df.columns)}")
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
        df.to_sql(table, con=engine, if_exists='replace', index=False)
        logging.info(f" Loaded '{table}' into MySQL, Rows: {len(df)}")
        
    else:
        logging.warning(f"File not found: {path}") 




