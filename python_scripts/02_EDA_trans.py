# -*- coding: utf-8 -*-
"""
Exploratory Data Analysis (EDA) for trans table, plotting different matrix using matplotlib package

input:  trans_cleaned.csv
output: various plots and csv saved in the working directory, 
        ./data/data_basetable_prep/trans_b.csv' -> aggregation of variables, prepare for the basetable merging
        
@author: Ekapope V
"""

###############################################################################
# Import libraries
import os
#os.chdir(r"D:\GitHub_IESEG\Python-Group-Project")
import numpy as np               
import pandas as pd              # DataFrame
import datetime
import matplotlib.pyplot as plt  # Visualization
import seaborn as sns            # Visualization
# set option, change the rows and cols max display 
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)
pd.options.display.float_format = '{0:.1f}'.format

# Import banking data
client = pd.read_csv('./data/data_berka/client.asc', sep=';')
account = pd.read_csv('./data/data_berka/account.asc', sep=';')
card = pd.read_csv('./data/data_berka/card.asc', sep=';')
disp = pd.read_csv('./data/data_berka/disp.asc', sep=';')


loan = pd.read_csv('./data/data_berka/loan.asc', sep=';')
district = pd.read_csv('./data/data_berka/district.asc', sep=';')

# EDA for trans
trans = pd.read_csv("./data/data_cleaned/trans_cleaned.csv",sep=';', index_col=0)
print(trans.info())
print(trans.describe().round(2))
print(trans.isnull().sum())
# % missing data
print((trans.isnull().sum()/len(trans)).round(2))

# replace 'NaN' with 'Unknown' for further plots
trans.trans_k_symbol.fillna('Unknown_Transaction_Type', inplace = True)

# function for plotting histogram, default bins = 20
# add summary stats on the right side, round to 1 decimal
def plot_histogram(df, col_name, bins=20):
    plt.hist(df[col_name], alpha=0.5, label=col_name, bins=bins)
    plt.legend(loc='upper right')
    plt.figtext(1.0, 0.2, df[col_name].describe().round(1))
    plt.title(col_name+' distribution')
    plt.margins(0.2)
    plt.savefig('./figures/Chris/fig_hist_'+str(col_name)+'.png', dpi=200, bbox_inches='tight')
    plt.show()
    print('./figures/Chris/fig_hist_'+str(col_name)+'.png')

# plot histogram order_amount (overall)
plot_histogram(trans, 'trans_amount')
plot_histogram(trans, 'balance_after_trans')

# Function that calculates the insight table
def create_pig_table(df, cont_var, cat_var):
    # Group by the variable you want to plot
    groups = df[[cont_var,cat_var]].groupby(cat_var)
    # Calculate the size and incidence of each group
    pig_table = groups[cont_var].agg(['mean','size']).reset_index()
    pig_table.rename(columns={'mean': 'mean_'+cont_var,'size': 'size'},inplace=True)
    return pig_table

# Discretize order_amount
trans['disc_trans_amount'] = pd.qcut(trans['trans_amount'], 5)
print(trans.groupby("disc_trans_amount").size())
# Re-cut, using round numbers
trans['disc_trans_amount'] = pd.cut(trans["trans_amount"],[0,100,2500,5000,10000,100000])
print(trans.groupby("disc_trans_amount").size())

# Create table by disc_order_amount grouping
pig_table = create_pig_table(trans,  "trans_amount" ,"disc_trans_amount")
print(pig_table)
pig_table.to_csv('./figures/Chris/fig_'+str('mean_trans_amount_VS_nbr_trans')+'.csv', header=True, sep=',')
width = 0.5
# plot the mean_order_amount/size
plt.ylim([0, 400000])
plt.ylabel("# of transactions", rotation = 90,rotation_mode="anchor", ha = "center" )
pig_table["mean_trans_amount"].plot(secondary_y = True)
pig_table["size"].plot(kind='bar', width = 0.5,color = "lightgray", edgecolor = "none") ## Add bars
plt.xticks(np.arange(len(pig_table)), pig_table["disc_trans_amount"], rotation = 45)
plt.xlim([-width, len(pig_table)-width])
plt.ylim([0, 30000])
plt.ylabel("mean_trans_amount", rotation = 90, rotation_mode="anchor", ha = "center")
plt.xlabel("disc_trans_amount")
plt.legend(loc='upper right')
plt.title('Average Transaction Amount (CZK) VS Number of Transactions')
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=2)
plt.margins(1)
plt.savefig('./figures/Chris/fig_'+str('mean_trans_amount_VS_nbr_trans')+'.png', dpi=200)
plt.show()


# Create table by order_k_symbol
pig_table = create_pig_table(trans,  "trans_amount" ,"trans_k_symbol")
print(pig_table)
pig_table.to_csv('./figures/Chris/fig_'+str('trans_k_symbol_VS_nbr_trans')+'.csv', header=True, sep=',')
width = 0.5
# plot the mean_order_amount/size
plt.ylim([0, 600000])
plt.ylabel("# of transactions", rotation = 90,rotation_mode="anchor", ha = "center" )
pig_table["mean_trans_amount"].plot(secondary_y = True)
pig_table["size"].plot(kind='bar', width = 0.5,color = "lightgray", edgecolor = "none") ## Add bars
# Show the group names
plt.xticks(np.arange(len(pig_table)), pig_table["trans_k_symbol"], rotation = 45)
plt.xlim([-width, len(pig_table)-width])
plt.ylim([0, 12000])
plt.ylabel("mean_trans_amount", rotation = 90, rotation_mode="anchor", ha = "center")
plt.xlabel("characterization of the transactions",rotation=0)
plt.legend(loc='upper right')
plt.margins(1)
plt.title('Average Transaction Amount (CZK) VS Number of Transactions \n by Characterization of the transactions')
plt.savefig('./figures/Chris/fig_'+str('trans_k_symbol_VS_nbr_trans')+'.png', dpi=200)
plt.show()

# Create table by trans_type
# replace 'NaN' with 'Unknown' for further plots
trans.trans_type.fillna('Unknown_Transaction_Type', inplace = True)
pig_table = create_pig_table(trans,  "trans_amount" ,"trans_type")
print(pig_table)
pig_table.to_csv('./figures/Chris/fig_'+str('trans_type_VS_nbr_trans')+'.csv', header=True, sep=',')
width = 0.5
# plot the mean_order_amount/size
plt.ylim([0, 750000])
plt.ylabel("# of transactions", rotation = 90,rotation_mode="anchor", ha = "center" )
pig_table["mean_trans_amount"].plot(secondary_y = True)
pig_table["size"].plot(kind='bar', width = 0.5,color = "lightgray", edgecolor = "none") ## Add bars
plt.xticks(np.arange(len(pig_table)), pig_table["trans_type"], rotation = 45)
plt.xlim([-width, len(pig_table)-width])
plt.ylim([0, 15000])
plt.xlabel("Transaction Type")
plt.ylabel("mean_order_amount", rotation = 90, rotation_mode="anchor", ha = "center")
plt.legend(loc='upper right')
plt.title('Average Order Amount (CZK) VS Numbers of Orders \n by Transaction Type ')
plt.subplots_adjust(hspace=1)
plt.savefig('./figures/Chris/fig_'+str('trans_type_VS_nbr_trans')+'.png', dpi=200)
plt.show()


# plot histogram order_amount (group by customer ID)
trans_amount_group_id = trans.groupby('account_id')['trans_amount'].agg(['sum','mean','size']).reset_index()
trans_amount_group_id.rename(columns={'sum': 'alltime_sum_trans_amount_by_account_id','mean': 'alltime_mean_trans_amount_by_account_id','size': 'alltime_total_nbr_trans'},inplace=True)
print(trans_amount_group_id.head())
print(trans_amount_group_id.describe())     

plot_histogram(trans_amount_group_id, 'alltime_sum_trans_amount_by_account_id')
plot_histogram(trans_amount_group_id, 'alltime_mean_trans_amount_by_account_id')

# group by customer ID, trans_k_symbol
trans_k_group_id = trans.groupby(['account_id','trans_k_symbol'])['trans_amount'].agg(['mean','size']).unstack().reset_index()
trans_k_group_id.rename(columns={'mean': 'mean_trans_amount_of','size': 'nbr_trans'},inplace=True)
# reset multi-index and rename colname
trans_k_group_id.columns = [' '.join(col).strip() for col in trans_k_group_id.columns.values]
print(trans_k_group_id.head())

# group by customer ID, trans_type
trans_type_group_id = trans.groupby(['account_id','trans_type'])['trans_amount'].agg(['mean','size']).unstack().reset_index()
trans_type_group_id.rename(columns={'mean': 'mean_trans_amount_of','size': 'nbr_trans'},inplace=True)
# reset multi-index and rename colname
trans_type_group_id.columns = [' '.join(col).strip() for col in trans_type_group_id.columns.values]
print(trans_type_group_id.head())



# cut the date interval
startdate = datetime.datetime(1993,1,1)
enddate = datetime.datetime(1999,1,1)
df_cut_list=[]
trans['date'] = pd.to_datetime(trans['date'], format='%Y-%m-%d')
def date_interval(df, agg_interval = [1,3]):
    for i in agg_interval:
        startdate = enddate-datetime.timedelta(i*365.25)
        interval = (df['date']>= startdate) & (df['date'] <= enddate)
        df_cut = trans[interval]
        df_cut = df_cut.groupby('account_id')['trans_amount'].agg(['sum','mean','size']).reset_index()
        df_cut.rename(columns={'sum': str(i)+'yr_sum_trans_amount_by_account_id','mean': str(i)+'yr_mean_trans_amount_by_account_id','size': str(i)+'yr_total_nbr_trans'},inplace=True)
        df_cut_list.append(df_cut)
    return(df_cut_list)
# assign aggregated by 2 interval (latest 1 yr, latest 3 yrs)    
df1,df2= date_interval(trans)
# number of days since last transaction (till enddate = datetime.datetime(1999,1,1)), for recency calculation
### Not useful
#trans['recency'] = enddate-trans['date']
#df3 = trans.groupby(['account_id'])['recency'].agg(['min']).unstack().reset_index()
#df3.rename(columns={'min': 'recency'},inplace=True)
#print(df3.describe())

# Calculate sum transaction growth in the 3 years
df_cut_list=[]
def sum_in_yr(df, agg_interval = [1,2,3]):
    enddate = datetime.datetime(1999,1,1)
    for i in agg_interval:
        startdate = enddate-datetime.timedelta((i)*365.25)
        enddate = enddate-datetime.timedelta((i-1)*365.25)
        interval = (df['date']>= startdate) & (df['date'] <= enddate)
        df_cut = df[interval]
        df_cut = df_cut.groupby('account_id')['trans_amount'].agg(['sum']).reset_index()
        df_cut.rename(columns={'sum': 'sum_trans_amount_by_account_id_in_yr'+str(startdate.year+1)},inplace=True)
        df_cut_list.append(df_cut)
    return(df_cut_list)
sum_per_yr_list= sum_in_yr(trans)


# make final aggregate table, one account id per row
trans_b = trans_amount_group_id.merge(trans_k_group_id, how='inner', left_on='account_id', right_on='account_id')
trans_b = trans_b.merge(trans_type_group_id, how='inner', left_on='account_id', right_on='account_id')
trans_b = trans_b.merge(df1, how='inner', left_on='account_id', right_on='account_id')
trans_b = trans_b.merge(df2, how='inner', left_on='account_id', right_on='account_id')

trans_bi = trans_b.merge(sum_per_yr_list[0], how='outer', left_on='account_id', right_on='account_id')
trans_bi = trans_bi.merge(sum_per_yr_list[1], how='outer', left_on='account_id', right_on='account_id')
trans_bi = trans_bi.merge(sum_per_yr_list[2], how='outer', left_on='account_id', right_on='account_id')

# Calculate rolling transaction growth in the last 2 years, trans_bi['trans_diff']
trans_bi['trans_ratio_98_97'] = trans_bi['sum_trans_amount_by_account_id_in_yr1998']/trans_bi['sum_trans_amount_by_account_id_in_yr1997']
trans_bi['trans_ratio_97_96'] = trans_bi['sum_trans_amount_by_account_id_in_yr1997']/trans_bi['sum_trans_amount_by_account_id_in_yr1996']

# drop intermediate cols
trans_bi= trans_bi.drop(['sum_trans_amount_by_account_id_in_yr1998',
                         'sum_trans_amount_by_account_id_in_yr1997',
                         'sum_trans_amount_by_account_id_in_yr1996'], axis=1)

# export to csv
trans_bi.to_csv('./data/data_basetable_prep/trans_b.csv', header=True, sep=';') 
print('export completed!') 




