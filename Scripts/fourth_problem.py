import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import scipy.stats as stats

from sqlalchemy import  text 
from config import get_engine

engine = get_engine() 


##how much of total procurement is dependent on top vendors? 
 #Total procurement (sum of all vendors' purchase dollars)


df=pd.read_sql(text("select * from vendor_sales_summary"),con=engine)

vendor_performance = df.groupby('VendorName').agg({'TotalPurchaseDollars':'sum','TotalSalesDollar':'sum','GrossProfit':'sum'}).reset_index()



total_procurement = vendor_performance['TotalPurchaseDollars'].sum() 

#consider top 10 vendors

top_vendor_procurement = vendor_performance.sort_values(by='TotalPurchaseDollars',ascending=False).head(10)['TotalPurchaseDollars'].sum()


#calculate percentage dependency.. 
dependency_percentage = (total_procurement /top_vendor_procurement )*100 



print(f"Total procurement:\n,{total_procurement:,.2f}") 
print(f"Top 10 vendor procurement:\n,{top_vendor_procurement:,.2f}") 
print(f"Dependency percentage:\n,{dependency_percentage:,.2f}") 


## draw donut chart
others = total_procurement - top_vendor_procurement
values = [top_vendor_procurement, others]

labels = [
    f"top 10 vendors({dependency_percentage:.1f}%)",
    f"others({100 - dependency_percentage:.1f}%)"
]
colors = ['blue','orange']
plt.figure(figsize=(8, 8))
plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
fig =plt.gcf()
fig.gca().add_artist(centre_circle)

plt.title("Procurement dependency: Top 10 vendors vs other")
plt.tight_layout()
plt.show()

















