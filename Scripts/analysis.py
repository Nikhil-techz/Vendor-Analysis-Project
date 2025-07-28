import pandas as pd
import time 
from sqlalchemy import inspect, text 
from config import get_engine
start = time.time()
engine = get_engine()

## this is load the sales csv file. 
sale = pd.read_csv("E:/Vendor Project/Data/sale.csv",low_memory=False) 
purchase = pd.read_csv("E:/Vendor Project/Data/Purchases.csv") 
vendors = pd.read_csv("E:/Vendor Project/Data/vendor_invoice.csv") 
purchase_prices = pd.read_csv("E:/Vendor Project/Data/Purchase_prices.csv") 


print("column of sales table: ",sale.columns.tolist())
print("Columns of Purchase:", purchase.columns.tolist()) 
print("vendor invoice column:",vendors.columns.tolist())
print("purchase prices column:",purchase_prices.columns.tolist())   


result = sale.groupby('Brand')[['SalesDollars','SalesPrice','SalesQuantity']].sum()
print(result) 

results= purchase.groupby(['Brand', 'PurchasePrice'])[['Quantity', 'Dollars']].sum()
print(results) 




## this is sql query for sum of freight cost from vendor_invoice table. 

query_result = pd.read_sql("select VendorNumber,sum(Freight) as freight_cost from vendor_invoice vi group by VendorNumber",con=engine)   
print("freight cost is : ",query_result)  

 

##fetch the data form purchase and purchase_price table. 
query = pd.read_sql("""
    SELECT 
        p.VendorNumber,
        p.VendorName,
        p.Brand,
        p.PurchasePrice,
        pp.Volume,
        pp.Price AS actual_price,
        SUM(p.Quantity) AS total_purchase_quantity,
        SUM(p.Dollars) AS total_purchase_dollars
    FROM purchases p
    JOIN vendorsdetail.purchase_price pp ON p.Brand = pp.Brand
    GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.PurchasePrice, pp.Volume, pp.Price
    ORDER BY total_purchase_dollars DESC
""", con=engine)

print(query) 



##fetch the data of sales table. 

queries = pd.read_sql(""" 
     select VendorNo, 
            
            Brand,
            sum(SalesDollars) as total_sales_dollars,
            sum(SalesQuantity) as total_sales_quantity,
            sum(ExciseTax) as total_excise_tax,
            sum(SalesPrice) as total_sales_price 
            from sale s 
            group by VendorNo, 
             
            
            Brand"""
            ,con=engine) 
print(queries)



final_query = """
WITH Freightsummary AS (
    SELECT 
        VendorNumber,
        SUM(Freight) AS freightcost 
    FROM vendor_invoice 
    GROUP BY VendorNumber
),

Purchasesummary AS (
    SELECT 
        p.VendorNumber,
        p.VendorName,
        p.Brand,
        p.Description,
        p.PurchasePrice,
        pp.Price AS ActualPrice,
        pp.Volume,
        SUM(p.Quantity) AS TotalPurchaseQuantity,
        SUM(p.Dollars) AS TotalPurchaseDollars
    FROM purchases p 
    JOIN purchase_price pp 
        ON p.Brand = pp.Brand
    GROUP BY 
        p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price, pp.Volume
),

SalesSummary AS (
    SELECT 
        VendorNo,
        Brand,
        SUM(SalesQuantity) AS TotalSalesQuantity,
        SUM(SalesDollars) AS TotalSalesDollar,
        SUM(SalesPrice) AS TotalSalesPrice,
        SUM(ExciseTax) AS TotalExciseTax
    FROM sale 
    GROUP BY VendorNo, Brand
)

SELECT 
    ps.VendorNumber,
    ps.VendorName,
    ps.Brand,
    ps.Description,
    ps.PurchasePrice,
    ps.ActualPrice,
    ps.Volume,
    ps.TotalPurchaseQuantity,
    ps.TotalPurchaseDollars,
    ss.TotalSalesQuantity,
    ss.TotalSalesDollar,
    ss.TotalSalesPrice,
    ss.TotalExciseTax,
    fs.freightcost
FROM Purchasesummary ps
LEFT JOIN SalesSummary ss
    ON ps.VendorNumber = ss.VendorNo
    AND ps.Brand = ss.Brand
LEFT JOIN Freightsummary fs
    ON ps.VendorNumber = fs.VendorNumber
ORDER BY ps.TotalPurchaseDollars DESC;
"""

## this function is merge all the query and create a cleaned table. 
def vendor_summary(engine):
    df = pd.read_sql_query(final_query,con=engine)
    return df



## --this function clean the data. --
def clean_data(df):
    ## changing the datatype .
    df['Volume'] = pd.to_numeric(df['Volume'],errors='coerce').astype('float')

    ##remove space from VendorName.

    df['VendorName'] = df['VendorName'].astype(str).str.strip()

    ## removing the null values with 0 . 

    df.fillna(0,inplace=True)

    df['GrossProfit'] = df['TotalSalesDollar'] - df['TotalPurchaseDollars'] 
    
    df['ProfitMargin'] = (df['GrossProfit'] / df['TotalSalesDollar'])*100
    df.loc[df['TotalSalesDollar']==0,'ProfitMargin']=0

    df['StockTurnOver'] = df['TotalSalesQuantity'] / df['TotalPurchaseQuantity'] 
    df.loc[df['TotalPurchaseQuantity']==0,'StockTurnOver']=0

    df['SalestoPurchaseRatio'] = df['TotalSalesDollar'] /df['TotalPurchaseDollars']
    df.loc[df['TotalPurchaseDollars']==0,'SalestoPurchaseRatio']=0
    return df


def get_cleaned_vendor_summary():
    engine = get_engine()
    df = vendor_summary(engine) 
    return clean_data(df) 

vendor_summary_table = vendor_summary(engine)
vendor_summary_table = clean_data(vendor_summary_table) 
print("final clean table: \n",vendor_summary_table) 
print("checking null values:\n",vendor_summary_table.isnull().sum())  
print("data type\n",vendor_summary_table.dtypes) 
# print("column are:",vendor_summary_table.columns.tolist())
 







end = time.time() 
print("Time Taken:",end-start,"seconds") 