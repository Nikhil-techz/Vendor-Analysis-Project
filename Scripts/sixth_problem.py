import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import scipy.stats as stats

from sqlalchemy import  text 
from config import get_engine

engine = get_engine() 


## how much capital is locked in unsold inventory  and which venodors contribute to most it?

df=pd.read_sql(text("select * from vendor_sales_summary"),con=engine) 

#make a column unsold_inventory
df['unsold_inventory'] =(df['TotalPurchaseQuantity'] - df['TotalSalesQuantity'])*df['PurchasePrice'] 

total_unsold_inventory = df['unsold_inventory'].sum() 

print("Total unsold inventory",total_unsold_inventory)  




 
# first group by:
vendor_unsold = df.groupby('VendorName')['unsold_inventory'].sum().sort_values(ascending=False) 



## plot a bar

plt.figure(figsize=(10,8)) 
sns.barplot(x=vendor_unsold.index[:10],y=vendor_unsold.values[:10],palette='Blues_r')
plt.xticks(rotation=45,ha='right')
plt.ylabel("capital locked in unsold inventory")
plt.xlabel("vendors")

plt.tight_layout()
plt.show()  

