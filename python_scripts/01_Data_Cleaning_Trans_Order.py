# -*- coding: utf-8 -*-
"""

Data cleaning for trans and order tables, using def functions and pandas

input:  trans.asc, order.asc
output: trans.csv, order.csv saved in the working directory ./data/data_cleaned/

@author: Ekapope V

"""
###############################################################################
# Using code from the class room
###############################################################################

# Import libraries
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

# Transform the birth day into year
client['birth_year'] = client['birth_number'].transform(lambda bn: int('19' + str(bn)[:2]))

# Age
client['age'] = 1999 - client['birth_year']

# Age group
client['age_group'] = client['age'] // 10 * 10

# Function to extract birth month and gender
def to_month_gender(birth_number):
    
    s = str(birth_number)
    birth_month = int(s[2:4])
    
    if birth_month > 50:
        gender = "F"
        birth_month = birth_month - 50
    else:
        gender = 'M'
        
    return pd.Series({'birth_month':birth_month, 'gender':gender})

client[['birth_month', 'gender']] = client['birth_number'].apply(to_month_gender)


# Merge the client, disp and loan tables
client_acc = pd.merge(client, disp, on='client_id', how='left')
client_loan = pd.merge(client_acc, loan, on='account_id', how='left')
client_loan.head()

###############################################################################
# Clean transaction table
###############################################################################
trans = pd.read_csv('./data/data_berka/trans.asc', sep=';', low_memory=False)
# def functions: convert to English (Refer to transaction table's remarks)
# using if-else, return NaN for unmatched values
def convert_trans_type_to_eng(x):
    if x == 'PRIJEM':
        return 'Credit'
    elif x == 'VYDAJ':
        return 'Withdrawal'
    else:
        return np.NaN
    
def convert_trans_op_to_eng(x):
    if x == 'VYBER KARTOU':
        return 'Credit card withdrawal'
    elif x == 'VKLAD':
        return 'Credit in cash'
    elif x == 'PREVOD Z UCTU':
        return 'Collection from another bank'
    elif x == 'VYBER':
        return 'Withdrawal in Cash'
    elif x == 'PREVOD NA UCET':
        return 'Remittance to another bank'    
    else:
        return np.NaN
    
def convert_trans_k_symbol_to_eng(x):
    if x == 'POJISTNE':
        return 'Insurance payment'
    elif x == 'SLUZBY':
        return 'Payment for statement'
    elif x == 'UROK':
        return 'Interest credited'
    elif x == 'SANKC. UROK':
        return 'Sanction interest if negative balance'
    elif x == 'SIPO':
        return 'Household'
    elif x == 'DUCHOD':
        return 'Old-age pension'  
    elif x == 'UVER':
        return 'Loan payment'      
    else:
        return np.NaN
    
# use map to apply above functions to type, operation, amount columns
trans['trans_type'] = trans['type'].map(convert_trans_type_to_eng)
trans['trans_operation'] = trans['operation'].map(convert_trans_op_to_eng)
trans['trans_k_symbol'] = trans['k_symbol'].map(convert_trans_k_symbol_to_eng)

# drop original columns after modified
trans=trans.drop(['type', 'operation','k_symbol'], axis=1)

# converts the date into a proper date format
trans['date'] = pd.to_datetime(trans['date'], format='%y%m%d')

# rename the column names as per remarks
trans = trans.rename(columns={'amount': 'trans_amount',
                              'balance':'balance_after_trans',
                              'bank':'trans_bank_partner',
                              'account':'trans_account_partner'})
# check the info and samples
print(trans.info())
print(trans.sample(5))

# export to csv
trans.to_csv('./data/data_cleaned/trans_cleaned.csv', header=True, sep=';') 
print('export completed!')

###############################################################################
# Clean order table
###############################################################################
order = pd.read_csv('./data/data_berka/order.asc', sep=';')
# def function: convert to English (Refer to order table's remarks)
# use the same translation as transaction table to keep the integrity
# use if-else, return NaN for unmatched values
def convert_order_k_symbol_to_eng(x):
    if x == 'POJISTNE':
        return 'Insurance payment'
    elif x == 'SIPO':
        return 'Household'
    elif x == 'LEASING':
        return 'Leasing'
    elif x == 'UVER':
        return 'Loan payment'
    else:
        return np.NaN

# use map, apply to k_symbol
order['order_k_symbol'] = order['k_symbol'].map(convert_order_k_symbol_to_eng)
# drop original columns after modified
order=order.drop(['k_symbol'], axis=1)
# rename the column names as per remarks
order = order.rename(columns={'bank_to': 'order_recipient_bank',
                              'account_to':'order_recipient_account',
                              'amount':'order_amount'})
    
    # check the info and samples
print(order.info())
print(order.sample(5))

# export to csv
order.to_csv('./data/data_cleaned/order_cleaned.csv', header=True, sep=';') 
print('export completed!')