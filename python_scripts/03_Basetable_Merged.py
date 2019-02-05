# -*- coding: utf-8 -*-
"""
Basetable merging

input:  all related *.csv files, located in  /data/data_basetable_prep/ and /data/data_cleaned/
output: basetable.csv

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
import seaborn as sns      

trans_b = pd.read_csv('./data/data_basetable_prep/trans_b.csv', sep=';')
order_b = pd.read_csv('./data/data_basetable_prep/order_b.csv', sep=';')
trans_b_order_b = trans_b.merge(order_b, how='outer', left_on='account_id', right_on='account_id')

cleaned_client= pd.read_csv('./data/data_cleaned/cleaned_client.csv', sep=',')
cleaned_account= pd.read_csv('./data/data_cleaned/cleaned_account.csv', sep=',')
cleaned_card= pd.read_csv('./data/data_cleaned/cleaned_card.csv', sep=',')
cleaned_disp= pd.read_csv('./data/data_cleaned/cleaned_disp.csv', sep=',')
cleaned_district= pd.read_csv('./data/data_cleaned/cleaned_district.csv', sep=',')
cleaned_loan= pd.read_csv('./data/data_cleaned/cleaned_loan.csv', sep=',')

basetable = cleaned_client.merge(cleaned_disp, how='outer', left_on='client_id', right_on='client_id')
basetable = basetable.merge(trans_b_order_b, how='outer', left_on='account_id', right_on='account_id')
basetable = basetable.merge(cleaned_account, how='outer', left_on='account_id', right_on='account_id')
basetable = basetable.merge(cleaned_loan, how='outer', left_on='account_id', right_on='account_id')
basetable = basetable.merge(cleaned_disp, how='outer', left_on='disp_id', right_on='disp_id')
basetable = basetable.merge(cleaned_card, how='outer', left_on='disp_id', right_on='disp_id')
basetable = basetable.merge(cleaned_district, how='outer', left_on='client_district_id', right_on='district_id')
print(list(basetable))
basetable= basetable.drop(['Unnamed: 0_x', 'Unnamed: 0_y','client_id_y', 'account_id_y', 'type_y'], axis=1)

basetable.columns = basetable.columns.str.replace(r'_x', '')
basetable.columns = basetable.columns.str.replace(r'_y', '')
basetable.columns = basetable.columns.str.replace(r' ', '_')

final_colnames = list(basetable)
# export to csv
basetable.to_csv('./data/basetable.csv', header=True, sep=',') 
print(list(basetable))
print('export completed!') 
