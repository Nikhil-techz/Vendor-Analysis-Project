import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import scipy.stats as stats

from sqlalchemy import  text 
from config import get_engine

engine = get_engine() 


## which inventory have low turn over, indicating access stock and slow moving products: 

df=pd.read_sql(text("select * from vendor_sales_summary"),con=engine)

vendor_performance = (df [df['StockTurnOver']<1].groupby('VendorName')['StockTurnOver'].mean().sort_values(ascending=True).head(10) )

print("stock Turn over:",vendor_performance)
