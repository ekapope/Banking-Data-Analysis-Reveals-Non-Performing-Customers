# -*- coding: utf-8 -*-
"""

Basetable analysis, plotting different matrix using seaborn package

input:  basetable.csv
output: various plots saved in the working directory,
        ./data/top10percent_customer.csv', ./data/bottom10percent_customer.csv -> top10% and bottom10% customers, more details in datamart PDF report

@author: Ekapope V
"""
import os
os.chdir(r"C:\Users\eviriyakovithya\Documents\GitHub\Python-Group-Project")
import numpy as np               
import pandas as pd              # DataFrame
import datetime
import matplotlib.pyplot as plt  # Visualization
import seaborn as sns 
import time
basetable= pd.read_csv('./data/basetable.csv', sep=',', index_col=0)

basetable.columns = basetable.columns.str.replace(r'.1', '')
basetable.columns = basetable.columns.str.replace(r'.2', '')
basetable.columns = basetable.columns.str.replace(r'.3', '')
basetable_col_list = pd.DataFrame(list(basetable))
# export all column names for data mart report
basetable_col_list.to_csv('./data/basetable_col_list.csv', header=True, sep=',')
###############################################################################
#jointplot
sns.set(style="darkgrid")
x_cols = ['client_age']
y_cols = [col for col in basetable.columns if 'order' in col]
for x_col in x_cols:
    for y_col in y_cols:
        g = sns.jointplot(x_col, y_col, data=basetable, color="b",kind="hex", height =7, joint_kws={"alpha": 0.4})
        g.savefig('./figures/Chris/Basetable_Analysis/JointPlot'+'_'+str(x_col)+'_VS_'+str(y_col)+'.png', dpi=200)
###############################################################################    
allcols=list(basetable)
# Grouped Scatter plots
start_time = time.time()
sns.set(style="ticks")
#cat_cols = list(basetable.select_dtypes(include='object').columns)
#cat_cols.remove('district_name')
cat_cols = ['client_gender', 'type', 'statement_freq', 'loan_status', 'card_type', 'region']
x_cols = ['client_age']
y_cols = [col for col in basetable.columns if 'order' in col]
for cat_col in cat_cols:
    for x_col in x_cols:
        for y_col in y_cols:
            g = sns.lmplot(x=x_col, y=y_col,col=cat_col, hue=cat_col, data=basetable,
                       col_wrap=4, ci=None, palette="muted",fit_reg=False,
                       scatter_kws={"s": 50, "alpha": 0.2})
            g.savefig('./figures/Chris/Basetable_Analysis/ScatterPlot_by_'+str(cat_col)+'_'+str(x_col)+'_VS_'+str(y_col)+'.png', dpi=200)
    print("total time taken :", time.time() - start_time)
print("total time taken :", time.time() - start_time)
###############################################################################
#Pair plots
sns.set(style="ticks", color_codes=True)

basetable_pp=basetable.copy()
basetable_pp.columns = basetable_pp.columns.str.replace(r'mean_order_amount', 'MO')
pairplot_cols = ['MO_of_Household', 
                 'MO_of_Insurance_payment',
                 'MO_of_Loan_payment']
cat_cols = ['client_gender', 'type', 'statement_freq', 'card_type', 'loan_status', 'region']
for cat_col in cat_cols:
    g = sns.pairplot(basetable_pp,vars=pairplot_cols, hue=cat_col,plot_kws={"alpha": 0.2})
    g.savefig('./figures/Chris/Basetable_Analysis/PairPlot_by_'+str(cat_col)+'.png', dpi=200)
        
###############################################################################    
# find the top 10% of transaction growth
    
basetable_sorted= basetable.sort_values(by=['trans_ratio_98_97'], ascending=False)

# export top 10% and last 10% growth
basetable_sorted.head(round(0.1*len(basetable_sorted))).to_csv('./data/top10percent_customer.csv', header=True, sep=',') 
basetable_sorted.tail(round(0.1*len(basetable_sorted))).to_csv('./data/bottom10percent_customer.csv', header=True, sep=',') 
    

###############################################################################
#jointplot
sns.set(style="darkgrid")
x_cols = ['client_age']
y_cols = [col for col in basetable.columns if 'trans' in col]
for x_col in x_cols:
    for y_col in y_cols:
        g = sns.jointplot(x_col, y_col, data=basetable, color="b",kind="hex", height =7, joint_kws={"alpha": 0.4})
        g.savefig('./figures/Chris/Basetable_Analysis/JointPlot'+'_'+str(x_col)+'_VS_'+str(y_col)+'.png', dpi=200)   

############################################################################### 
#Grouped barplots
#sns.set(style="whitegrid")
#x_cols = ['type', 'statement_freq', 'loan_status', 'card_type', 'region']
#y_cols = [col for col in basetable.columns if 'order' in col]
#cat_cols = ['client_gender']
#for cat_col in cat_cols:
#    for x_col in x_cols:
#        for y_col in y_cols:
#            g = sns.catplot(x='type', y='mean_order_amount_of_Household',
#                            hue='client_gender', data=basetable,
#                            height=6, kind="bar", palette="muted")
#            g.despine(left=True)
#            g.set_ylabels(y_col)
#            g.savefig('./figures/Chris/Basetable_Analysis/BarPlot_by_'+str(cat_col)+'_'+str(x_col)+'_VS_'+str(y_col)+'.png', dpi=200)


