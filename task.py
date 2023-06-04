import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import LabelEncoder
import sqlite3
#first create empty database named fastfood.db
Path('fastfood.db').touch()
#connect to database
conn = sqlite3.connect('fastfood.db')
c = conn.cursor()
#read csv file
data = pd.read_csv(r'fastfood.csv')   
df = pd.DataFrame(data)
#store dataframe in database
df.to_sql('df', conn, if_exists='replace', index = False)
#read data from database in dataframe
data=pd.read_sql("select * from df",conn)
#print dataframe
print(data)
#Average,minimum and maximum of calories
print("Maximum caleries:",max(data["calories"]))
print("Minimum caleries:",min(data["calories"]))
print("Average caleries:",data["calories"].mean())
#rank the restaurant by average
data["avg_rank"]=data.groupby("restaurant")["calories"].rank(method="average",ascending=True)
#Top 5 data based on rank
print(data.head())
#visulization
plt.plot(data.loc[0:5,'restaurant'],data.loc[0:5,'avg_rank'])
#saved plot in plot1.png file
plt.savefig('plot1.png')
def trans(category,item):
    if category=="Main":
        if 'Chicken' in item:
            return 'Chicken'
        elif 'Beef' in item:
            return 'Beef'
        elif 'Seafood' in item:
            return 'Seafood'
        elif 'Pork' in item :
            return 'Pork'
        else:
            return 'Other'
    else:
        return None
#categories item based on calories into Main,Sde and Dessert
data["category"]=pd.cut(np.array(data["calories"]),3,labels=["Main","Side","Dessert"])
#sub-categories where category is Main 
data["sub_category"]=data.apply(lambda x:trans(x["category"],x["item"]),axis=1)
print(data)
#export data to csv
data.to_csv('food_cats.csv')
