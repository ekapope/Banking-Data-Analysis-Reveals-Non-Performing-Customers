# -*- coding: utf-8 -*-
"""
Exploratory Data Analysis (EDA) for order table, plotting different matrix using matplotlib package

input:  order_cleaned.csv
output: various plots and csv saved in the working directory, 
        ./data/data_basetable_prep/order_b.csv -> aggregation of variables, prepare for the basetable merging

@author: Ekapope V        
"""

###############################################################################
# Import libraries
import os
#os.chdir(r"D:\GitHub_IESEG\Python-Group-Project")
import numpy as np               
import pandas as pd              # DataFrame
import matplotlib.pyplot as plt  # Visualization
import seaborn as sns            # Visualization
# set option, change the rows and cols max display 
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)

# Import banking data
client = pd.read_csv('./data/data_berka/client.asc', sep=';')
account = pd.read_csv('./data/data_berka/account.asc', sep=';')
card = pd.read_csv('./data/data_berka/card.asc', sep=';')
disp = pd.read_csv('./data/data_berka/disp.asc', sep=';')


loan = pd.read_csv('./data/data_berka/loan.asc', sep=';')
district = pd.read_csv('./data/data_berka/district.asc', sep=';')

# EDA for order 
order = pd.read_csv('./data/data_cleaned/order_cleaned.csv',sep=';', index_col=0)
print(order.info())
print(order.describe())
print(order.isnull().sum())
# % missing data
print(order.isnull().sum()/len(order))

# replace 'NaN' with 'Unknown' for further plots
order.order_k_symbol.fillna('Unknown_Order_Type', inplace = True)


# Function that calculates the insight table
def create_pig_table(df, cont_var, cat_var):
    # Group by the variable you want to plot
    groups = df[[cont_var,cat_var]].groupby(cat_var)
    # Calculate the size and incidence of each group
    pig_table = groups[cont_var].agg(['mean','size']).reset_index()
    pig_table.rename(columns={'mean': 'mean_'+cont_var,'size': 'size'},inplace=True)
    return pig_table

# Discretize order_amount
order['disc_order_amount'] = pd.qcut(order['order_amount'], 5)
print(order.groupby("disc_order_amount").size())
# Re-cut, using round numbers
order['disc_order_amount'] = pd.cut(order["order_amount"],[0,3000,5000,10000,15000])
print(order.groupby("disc_order_amount").size())

# Create table by disc_order_amount grouping
pig_table = create_pig_table(order,  "order_amount" ,"disc_order_amount")
print(pig_table)
width = 0.5
pig_table.to_csv('./figures/Chris/order/fig_'+str('mean_order_amount_VS_nbr_orders')+'.csv', header=True, sep=',')
# plot the mean_order_amount/size
plt.ylabel("# of orders", rotation = 90,rotation_mode="anchor", ha = "center" )
pig_table["mean_order_amount"].plot(secondary_y = True)
pig_table["size"].plot(kind='bar', width = 0.5,color = "lightgray", edgecolor = "none") ## Add bars
plt.xticks(np.arange(len(pig_table)), pig_table["disc_order_amount"], rotation = 45)
plt.xlim([-width, len(pig_table)-width])
plt.ylim([0, 15000])
plt.ylabel("mean_order_amount", rotation = 90, rotation_mode="anchor", ha = "center")
plt.xlabel("disc_order_amount")
plt.legend(loc='upper right')
plt.title('Average Order Amount ($) VS Numbers of Orders \n by group')
#plt.tight_layout()
plt.savefig('./figures/Chris/order/fig_'+str('mean_order_amount_VS_nbr_orders')+'.png', dpi=200)
plt.show()


# Create table by order_k_symbol
pig_table = create_pig_table(order,  "order_amount" ,"order_k_symbol")
print(pig_table)
width = 0.5
pig_table.to_csv('./figures/Chris/order/fig_'+str('order_k_symbol_VS_nbr_orders')+'.csv', header=True, sep=',')
# plot the mean_order_amount/size
plt.ylabel("# of orders", rotation = 90,rotation_mode="anchor", ha = "center" )
pig_table["mean_order_amount"].plot(secondary_y = True)
pig_table["size"].plot(kind='bar', width = 0.5,color = "lightgray", edgecolor = "none") ## Add bars
# Show the group names
plt.xticks(np.arange(len(pig_table)), pig_table["order_k_symbol"], rotation = 45)
plt.xlim([-width, len(pig_table)-width])
plt.ylim([0, 6000])
plt.ylabel("mean_order_amount", rotation = 90, rotation_mode="anchor", ha = "center")
plt.xlabel("characterization of the payment")
plt.legend(loc='upper right')
plt.title('Average Order Amount ($) VS Numbers of Orders \n by Characterization of the payment')
#plt.tight_layout()
plt.savefig('./figures/Chris/order/fig_'+str('order_k_symbol_VS_nbr_orders')+'.png', dpi=200)
plt.show()

# Create table by order_recipient_bank
pig_table = create_pig_table(order,  "order_amount" ,"order_recipient_bank")
print(pig_table)
width = 0.5
pig_table.to_csv('./figures/Chris/order/fig_'+str('order_recipient_bank_VS_nbr_orders')+'.csv', header=True, sep=',')
# plot the mean_order_amount/size
plt.ylabel("# of orders", rotation = 90,rotation_mode="anchor", ha = "center" )
pig_table["mean_order_amount"].plot(secondary_y = True)
pig_table["size"].plot(kind='bar', width = 0.5,color = "lightgray", edgecolor = "none") ## Add bars
# Show the group names
plt.xticks(np.arange(len(pig_table)), pig_table["order_recipient_bank"], rotation = 45)
plt.xlim([-width, len(pig_table)-width])
plt.ylim([0, 4000])
plt.ylabel("mean_order_amount", rotation = 90, rotation_mode="anchor", ha = "center")
plt.xlabel("characterization of the payment")
plt.legend(loc='upper right')
plt.title('Average Order Amount ($) VS Numbers of Orders \n by Bank of the recipient')
#plt.tight_layout()
plt.savefig('./figures/Chris/order/fig_'+str('order_recipient_bank_VS_nbr_orders')+'.png', dpi=200)
plt.show()


# function for plotting histogram, default bins = 20
# add summary stats on the right side, round to 1 decimal
def plot_histogram(df, col_name, bins=20):
    plt.hist(df[col_name], alpha=0.5, label=col_name, bins=bins)
    plt.legend(loc='upper right')
    plt.figtext(1.0, 0.2, df[col_name].describe().round(1))
    plt.title(col_name+' Distribution')
    plt.savefig('fig_hist_'+str(col_name)+'.png', dpi=200, bbox_inches='tight')
    plt.show()
    print('./figures/Chris/order/fig_hist_'+str(col_name)+'.png')

# plot histogram order_amount (overall)
plot_histogram(order, 'order_amount')

# plot histogram order_amount (group by customer ID)
order_amount_group_id = order.groupby('account_id')['order_amount'].agg(['sum','mean','size']).reset_index()
order_amount_group_id.rename(columns={'sum': 'sum_order_amount_by_account_id','mean': 'mean_order_amount_by_account_id','size': 'total_nbr_orders'},inplace=True)
print(order_amount_group_id.head())
print(order_amount_group_id.describe())     

plot_histogram(order_amount_group_id, 'sum_order_amount_by_account_id')
plot_histogram(order_amount_group_id, 'mean_order_amount_by_account_id')

# group by customer ID, order_k_symbol
order_type_group_id = order.groupby(['account_id','order_k_symbol'])['order_amount'].agg(['mean','size']).unstack().reset_index()
order_type_group_id.rename(columns={'mean': 'mean_order_amount_of','size': 'nbr_orders'},inplace=True)
print(order_type_group_id.head())
# reset multi-index and rename colname
order_type_group_id.columns = [' '.join(col).strip() for col in order_type_group_id.columns.values]

# make final aggregate table, one account id per row
order_b = order_amount_group_id.merge(order_type_group_id, how='inner', left_on='account_id', right_on='account_id')
# export to csv
order_b.to_csv('./data/data_basetable_prep/order_b.csv', header=True, sep=';') 
print('export completed!') 



#trans = pd.read_csv("./data/data_cleaned/trans_cleaned.csv",sep=';', index_col=0)


