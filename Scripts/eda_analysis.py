import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import scipy.stats as stats

from sqlalchemy import  text 
from config import get_engine

engine = get_engine() 

df = pd.read_sql(text("select * from vendor_sales_summary"),con=engine) 
print(df.columns.tolist()) 
print(df.describe().T) 

###----- this query is for filte out the data , to remove the inconsistency . ----  

df=pd.read_sql(text("select * from vendor_sales_summary where GrossProfit>0 and ProfitMargin>0 and TotalSalesQuantity>0"),con=engine) 
print(df)


 ##distribute the plot for numerical columns after filter the data .
numerical_cols = df.select_dtypes(include=np.number).columns 
plt.figure(figsize=(15,10))
for i, cols in enumerate(numerical_cols):
    plt.subplot(4,4,i+1) 
    sns.histplot(df[cols],kde=True,bins=30) 
    plt.title(cols)

plt.tight_layout() 
plt.show()


##count plot for categorical column

categorical_cols = ["VendorName","Description"]
plt.figure(figsize=(12,5))
for i , cols in enumerate(categorical_cols):
    plt.subplot(1,2,i+1) 
    sns.countplot(y=cols,data=df,order=df[cols].value_counts().index[:10]) #top 10 vendor name,descriptio
    plt.title(f"count plot of {cols}")
plt.tight_layout()
plt.show()


##correlation heatmap

plt.figure(figsize=(12,5))
correlation_matrix = df[numerical_cols].corr()
sns.heatmap(correlation_matrix,annot=True,fmt=".2f",cmap="coolwarm",linewidth=0.5,cbar=True)
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.title("correlation heatmap") 
plt.show() 

