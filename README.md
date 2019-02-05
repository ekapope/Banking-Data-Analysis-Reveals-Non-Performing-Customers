# Datamart Report - PKDD'99 Discovery Challenge

The purpose of this report is to analyze the financial status of clients in Czech Republic between
January 1st ,1993 and December 31st, 1998. In order to create data mart, we used the following
datasets 1.Card 2.Client 3. Account 4.Trans 5. Orders 6.Loans 7.Demographics 8. Disp. The total
observations and variables of this data mart are 5,369 and 81 respectively


## Datamart (basetable) Analysis

‘trans_ratio_98_97’ column derives from the ratio of transaction growth in the past year. After sorted
this column descending, it reveals the top 10% customers with the most transaction growth in the past
year and also the bottom 10% which had the least transaction growth. With this information, the bank
can take appropriate action on this.

The client data was exported into two csv files; bottom10percent_customer.csv, top10percent_customer.csv.

#### Data source: 
[PKDD 1999, Discovery Challenge Guide to the Financial Data Set (1999)](http://lisp.vse.cz/pkdd99/Challenge/berka.htm)
