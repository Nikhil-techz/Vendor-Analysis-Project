import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import scipy.stats as stats

from sqlalchemy import  text 
from config import get_engine

engine = get_engine() 


#which vendor contribute most to total purchase dollars. 



df=pd.read_sql(text("select * from vendor_sales_summary"),con=engine)

vendor_performance = df.groupby('VendorName').agg({'TotalPurchaseDollars':'sum','TotalSalesDollar':'sum','GrossProfit':'sum'}).reset_index() 


#calculate purchase contribution
vendor_performance['PurchaseContribution %'] = (vendor_performance['TotalPurchaseDollars'] / vendor_performance['TotalPurchaseDollars'].sum())*100

top_purchase_vendors = vendor_performance.sort_values(by='TotalPurchaseDollars',ascending=False).head(10) 
print(top_purchase_vendors) 

##visualization 

plt.figure(figsize=(10,8))
sns.barplot(
    x=top_purchase_vendors['TotalPurchaseDollars'],
    y=top_purchase_vendors['VendorName'],
    palette = 'Blues_r')

plt.title("Top 10 vendors by total purchase distribution")
plt.xlabel("Total purchase Dollars")
plt.ylabel("Vendor Name")
plt.tight_layout()
plt.show() 


