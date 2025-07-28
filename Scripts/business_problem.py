import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import scipy.stats as stats

from sqlalchemy import  text 
from config import get_engine

engine = get_engine() 

#1:- identify the brands that needs promotional or pricing adjustment which exibits lower sales performance but higher profit margin.-- 

df =  pd.read_sql(text("select * from vendor_sales_summary"),con=engine) 
print(df.columns.to_list())


##create a new column ProfitDollar - in this assign profit and group by description .
# and calculate total sales and profit and stored in new column(otalSalesDollars,TotalProfitDollar)

brand_performance = (df.assign(ProfitDollar=df['TotalSalesDollar']* df['ProfitMargin']).groupby('Description',as_index=False).agg(TotalSalesDollars=('TotalSalesDollar','sum'),TotalProfitDollar=('ProfitDollar','sum')).assign(ProfitMargin=lambda d:d['TotalProfitDollar'] / d['TotalSalesDollars'])
      .drop(columns='TotalProfitDollar'))  

## now calculate the profitmargin by assigning  a new column.
#lambda d- means- current datafram call d. for calculation  



low_sale_threshold = 30000 #manually select sales  threshold and profit margin 
high_margin_threshold =  50

## find the value below 30 % sales and profit margin above 60 percent. 

#select only those brand who need promotional 

#

print(brand_performance[brand_performance['TotalSalesDollars']<low_sale_threshold]) 
print(brand_performance[brand_performance['ProfitMargin'] > high_margin_threshold])


##represent the value in "k" in thousand
brand_performance['TotalSalesDollars'] = (brand_performance['TotalSalesDollars']/1000).round(1) 
##draw scatterplot
plt.figure(figsize=(10,8))
 
plt.scatter(brand_performance['TotalSalesDollars'], brand_performance['ProfitMargin'],color='green') 


#marks threshold for lower sales and profit margin 
plt.axvline(x=low_sale_threshold,color='red',linestyle='--')
plt.axhline(y=high_margin_threshold,color='blue',linestyle='--') 
plt.xlabel("Total sales dollars")
plt.ylabel("Profit margin(%)") 
plt.title("Brand Performance: Sales vs Profit Margin") 

plt.grid(True) 
plt.show()



 


