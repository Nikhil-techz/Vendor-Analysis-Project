import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import scipy.stats as stats

from sqlalchemy import  text 
from config import get_engine

engine = get_engine() 

#-2:-which vendors and brands demonstrate the highest sales performance?

df=pd.read_sql(text("select * from vendor_sales_summary"),con=engine) 
top_vendors = df.groupby('VendorName')['TotalSalesDollar'].sum().nlargest(10)
top_brands= df.groupby('Description')['TotalSalesDollar'].sum().nlargest(10)
print("Top vendors\n",top_vendors)
print("Top brands\n",top_brands)  


##visulization for top brand and vendors by barplot.
# create two subplot one for top vendor and top brands.
plt.figure(figsize=(10,8)) 
plt.subplot(1,2,1)

sns.barplot(x=top_vendors.values,y=top_vendors.index,palette='Blues_r')
plt.title("Top 10 vendors by sales") 
plt.xlabel("Total sales $")
plt.ylabel("Vendors") 

plt.subplot(1,2,2) 
sns.barplot(x=top_brands.values,y=top_brands.index,palette='Reds_r')
plt.title("Top 10 brands by sales")
plt.xlabel("Total brands")
plt.tight_layout() 
plt.show() 
