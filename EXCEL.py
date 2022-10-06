import pandas as pd

headers = ['num','equipment','code','manufacturer','model', 'sn','prod_date','supp_date','del','del','del','del','del','del','location','terms','status','qrcode']
devices = pd.read_excel('./DB.xlsx',names=headers)
devices.drop(['del','del.1','del.2','del.3','del.4','del.5'], axis = 1, inplace = True) 

for i in range(1,len(devices)):
    print(devices["sn"].get(i))
