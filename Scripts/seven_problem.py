import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import scipy.stats as stats

from sqlalchemy import  text 
from config import get_engine

engine = get_engine() 

#calculate the lower performance of vendors  



df=pd.read_sql(text("select * from vendor_sales_summary"),con=engine) 

df['unsold_inventory'] = (df['TotalPurchaseQuantity'] - df['TotalSalesQuantity'] )*df['PurchasePrice']


# group by vendor name, unsold_inventory

vendor_performance = df.groupby('VendorName')['unsold_inventory'].sum().sort_values(ascending=False)

lower_performance_vendor= vendor_performance.head(10)
print("lower_performance_vendor", lower_performance_vendor) 
