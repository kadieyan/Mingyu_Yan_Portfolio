# -*- coding: utf-8 -*-
"""
**Parameters**
Store - the store number
Date - the week
Temperature - average temperature in the region
Fuel_Price - cost of fuel in the region
MarkDown1-5 - anonymized data related to promotional markdowns. MarkDown data is only available after Nov 2011, and is not available for all stores all the time. Any missing value is marked with an NA
CPI - the consumer price index
Unemployment - the unemployment rate
IsHoliday - whether the week is a special holiday week
Sales - Historical sales data, which covers to 2010-02-05 to 2012-11-01. Within this tab you will find the following fields:
Dept - the department number
Weekly_Sales -  sales for the given department in the given store

#Data processing
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import calendar  
import random
np.random.seed(42)
from matplotlib import pyplot

"""*Import Data*"""

#mounting drive
from google.colab import drive
drive.mount('/content/drive')

!ls /content/drive/'My Drive'/'Retail Analytics'/'S1.csv'
!ls /content/drive/'My Drive'/'Retail Analytics'/'S2.csv'
!ls /content/drive/'My Drive'/'Retail Analytics'/'S3.csv'

features = pd.read_csv("/content/drive/My Drive/Retail Analytics/S1.csv")
sales = pd.read_csv("/content/drive/My Drive/Retail Analytics/S2.csv")
stores = pd.read_csv("/content/drive/My Drive/Retail Analytics/S3.csv")

df=pd.merge(sales,features, on=['Store','Date', 'IsHoliday'], how='left')
df=pd.merge(df,stores, on=['Store'], how='left')
df_raw = df

df['Date'] = pd.to_datetime(df['Date'])

df = df.set_index('Date')

df.describe()

#Mean and SD of each markdown in each month in 2012
Dafr_2012 = df['2012']
DF_2012= Dafr_2012.loc[:,[x for x in Dafr_2012.columns if 'MarkDown' in x]]
Result_2012 = DF_2012.resample('M').agg(['mean','std'])
Result_2012

Dafr_2011 = df['2011']

DF_2011= Dafr_2011.loc[:,[x for x in Dafr_2011.columns if 'MarkDown' in x]]
Result_2011 = DF_2011.resample('M').agg(['mean','std'])
Result_2011

"""#Visualization"""

df.head()

df_1 = df.sort_values(by=["Date", "Store"])
df_1.head()

df_by_store= df_1.loc[:,[x for x in df_1.columns if 'Store'in x or 'Weekly_Sales'in x or 'Temperature'in x
                           or 'Price'in x or 'MarkDown' in x or 'CPI' in x or 'Unemployment' in x]]
df_by_store= df_by_store.groupby('Store').resample('M').agg({'Weekly_Sales':np.sum,
                                                             'Temperature':np.mean,
                                                             'Fuel_Price':np.mean,
                                                             'MarkDown1':np.sum,
                                                             'MarkDown2':np.sum,
                                                             'MarkDown3':np.sum,
                                                             'MarkDown4':np.sum,
                                                             'MarkDown5':np.sum,
                                                             'CPI':np.mean,
                                                             'Unemployment':np.mean
                                                             })

#Montly data of all stores together
df_allstore = df_by_store.reset_index('Date')
df_allstore = df_allstore.groupby('Date').agg({'Weekly_Sales':np.sum,
                                                             'Temperature':np.mean,
                                                             'Fuel_Price':np.mean,
                                                             'MarkDown1':np.sum,
                                                             'MarkDown2':np.sum,
                                                             'MarkDown3':np.sum,
                                                             'MarkDown4':np.sum,
                                                             'MarkDown5':np.sum,
                                                             'CPI':np.mean,
                                                             'Unemployment':np.mean
                                                             })

#Data Normalization
allstore = df_allstore.apply(lambda x: (x-np.min(x))/(np.max(x)-np.min(x)))
df_s=df_allstore

plt.figure(figsize = (14,8))
sns.set(style='darkgrid', context='notebook', font_scale=1.5, color_codes=True)


x=df_s.index

plt.bar(x, height=df_s['MarkDown1'],color='r',label='MarkDown1',width=30)
plt.bar(x, height=df_s['MarkDown2'],color='b',label='MarkDown2',bottom=df_s['MarkDown1'],width=30)
plt.bar(x, height=df_s['MarkDown3'],color='g',label='MarkDown3',bottom=df_s['MarkDown1']+df_s['MarkDown2'],width=30)
plt.bar(x, height=df_s['MarkDown4'],color='y',label='MarkDown4',bottom=df_s['MarkDown1']+df_s['MarkDown2']+df_s['MarkDown3'],width=30)
plt.bar(x, height=df_s['MarkDown5'],color='c',label='MarkDown5',bottom=df_s['MarkDown1']+df_s['MarkDown2']+df_s['MarkDown3']+df_s['MarkDown4'],width=30)

plt.legend(bbox_to_anchor=(1.3,0.9))
plt.ylabel('Total MarkDown', fontsize=20)
plt.xlabel('Date',fontsize=20)
plt.xticks(x,('2010-01','2010-02','2010-03','2010-04','2010-05','2010-06','2010-07','2010-08','2010-09','2010-10','2010-11','2010-12',
                  '2011-01','2011-02','2011-03','2011-04','2011205','2011-06','2011-07','2011-08','2011-09','2011-10','2011-11','2011-12',
                   '2012-01','2012-02','2012-03','2012-04','2012-05','2012-06','2012-07','2012-08','2012-09','2012-10','2012-11','2012-12'),fontsize=15,rotation=90)
plt.show()

plt.figure(figsize = (15,8))

x =df_s.index 
y=df_s['MarkDown1']
y1=df_s['MarkDown2']
y2=df_s['MarkDown3']
y3=df_s['MarkDown4']
y4=df_s['MarkDown5']


sns.lineplot(x,y,color='r',label='MarkDown1',lw=3)
sns.lineplot(x,y1,color='b',label='MarkDown2',lw=3)
sns.lineplot(x,y2,color='y',label='MarkDown3',lw=3)
sns.lineplot(x,y3,color='g',label='MarkDown4',lw=3)
sns.lineplot(x,y4,color='c',label='MarkDown5',lw=3)

plt.ylabel("MarkDown", fontsize=20, labelpad=15)
plt.xlabel("Date", fontsize=20, labelpad=15)
plt.legend(bbox_to_anchor=(1.0,0.9))
plt.xticks(x,('2010-01','2010-02','2010-03','2010-04','2010-05','2010-06','2010-07','2010-08','2010-09','2010-10','2010-11','2010-12',
                  '2011-01','2011-02','2011-03','2011-04','2011205','2011-06','2011-07','2011-08','2011-09','2011-10','2011-11','2011-12',
                   '2012-01','2012-02','2012-03','2012-04','2012-05','2012-06','2012-07','2012-08','2012-09','2012-10','2012-11','2012-12'),fontsize=15,rotation=90)
plt.show()

plt.figure(figsize = (12,12))

plt.bar(x = df_s.index, height = df_s.Weekly_Sales, width = 31)

plt.xlabel("Date", fontsize=20, labelpad=15)
plt.ylabel("Monthly Sales", fontsize=20, labelpad=15)
plt.xticks(x,('2010-01','2010-02','2010-03','2010-04','2010-05','2010-06','2010-07','2010-08','2010-09','2010-10','2010-11','2010-12',
                  '2011-01','2011-02','2011-03','2011-04','2011205','2011-06','2011-07','2011-08','2011-09','2011-10','2011-11','2011-12',
                   '2012-01','2012-02','2012-03','2012-04','2012-05','2012-06','2012-07','2012-08','2012-09','2012-10','2012-11','2012-12'),fontsize=15,rotation=90)
plt.show()

df_b = df_by_store

df_b = df_b.apply(lambda x: (x-np.min(x))/(np.max(x)-np.min(x)))

plt.figure(figsize = (6,6))

x=df_b['Temperature']
y=df_b['Weekly_Sales']

plt.scatter(x,y)

plt.xlabel('Temperature', fontsize=15)
plt.ylabel('Monthly Sales', fontsize=15)
plt.show()

plt.figure(figsize = (6,6))

x=df_b['CPI']
y=df_b['Weekly_Sales']

plt.xlabel('CPI', fontsize=15)
plt.ylabel('Monthly Sales', fontsize=15)

plt.scatter(x,y)
plt.show()

plt.figure(figsize = (6,6))

x=df_b['Fuel_Price']
y=df_b['Weekly_Sales']

plt.xlabel('Fuel Price', fontsize=15)
plt.ylabel('Monthly Sales', fontsize=15)

plt.scatter(x,y)
plt.show()

fig, axarr = plt.subplots(7, 7, sharex=True, sharey=True,figsize=(15,10))
s = 1
for i in range(0, 7):
    for j in range(0, 7):
        xxx = axarr[i,j].hist(df['Weekly_Sales'].loc[df['Store'] == s], 50);
        axarr[i,j].set_yscale('log')
        axarr[i,j].set_xscale('log')
        axarr[i,j].set_ylim(1,1e4)
        axarr[i,j].set_xlim(5e2,1e6)

        s += 1
fig.text(0.5, 0.04, 'Weekly Sales', ha='center')
fig.text(0.04, 0.5, 'Number', va='center', rotation='vertical')


"""#Predict Sales - Time Series

**Chain Weekly Sales**
"""

sum_sales = df_raw.groupby(by=['Date'])['Weekly_Sales'].sum()

df_sales = pd.DataFrame(sum_sales)
df_sales = df_sales.reset_index()
df_sales['Date'] = pd.to_datetime(df_sales['Date'])

df_sales.sort_values('Date', inplace=True)

df_sales.set_index(["Date"], inplace=True)

df_sales

max(df_sales['Weekly_Sales'])

plt.figure(figsize = (14,8))
sns.lineplot(df_sales.index,df_sales['Weekly_Sales'],color='c')
plt.ylim(30000000,90000000)

plt.show()

train = df_sales['Weekly_Sales'][0:115]
test = df_sales['Weekly_Sales'][115]

import statsmodels.api as sm
fig = plt.figure(figsize=(12,8))
 
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(train, lags=100,ax=ax1)
ax1.xaxis.set_ticks_position('bottom')
fig.tight_layout()
 
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(train, lags=100, ax=ax2)
ax2.xaxis.set_ticks_position('bottom')
fig.tight_layout()
plt.show()

"""**ARIMA**"""

model = sm.tsa.ARIMA(train, order=(1, 0, 1))
results = model.fit()
resid = results.resid 
fig = plt.figure(figsize=(12,8))
fig = sm.graphics.tsa.plot_acf(resid.values.squeeze(), lags=40)
plt.show()

model = sm.tsa.ARIMA(df_sales, order=(1, 0, 1))
results = model.fit()
predict_sunspots = results.predict(start=str('2011-10-14'),end=str('2012-12-10'),dynamic=False)
# print(predict_sunspots)
fig, ax = plt.subplots(figsize=(12, 8))
ax = df_sales.plot(ax=ax)
predict_sunspots.plot(ax=ax)
plt.show()

fore_sunspots = results.forecast(steps=56)[0]

future_date = np.array(range(144,200)).reshape(-1, 1)

df_future_sales = pd.DataFrame(future_date)
df_future_sales.columns = ['Date']
df_future_sales['WeeklySales'] = fore_sunspots


plt.figure(figsize = (14,8))
sns.lineplot(df_future_sales['Date'],df_future_sales['WeeklySales'],color='c')
plt.ylim(30000000,90000000)

plt.show()

"""Which store has the worst performance"""

store_sales = df_raw.groupby(by=['Store'])['Weekly_Sales'].sum()
store_size = df_raw.groupby(by=['Store'])['Size'].mean()

df_store = pd.concat([store_sales, store_size], axis=1) 
# df_store
for i in range(0,len(df_store['Size'])):
  df_store['Weekly_Sales'][i:i+1] = df_store['Weekly_Sales'][i:i+1] / df_store['Size'][i:i+1]

# df_store

df_store.sort_values('Weekly_Sales', inplace=True)
df_store[0:1]

"""Conbine Data by "Store" and "Date""""

just_dummies = pd.get_dummies(df_raw['Type'])

df_raw = pd.concat([df_raw, just_dummies], axis=1)  
df_raw.rename(columns={"A": "TypeA","B": "TypeB","C": "TypeC"}, inplace = True)
df_raw = df_raw.drop(['Type'], axis=1)

holiday = np.array(df_raw["IsHoliday"])
holiday_bi = holiday.astype(int)
df_raw["IsHoliday"] = holiday_bi

df_c_1 = df_raw.groupby(by=['Date','Store'])['Weekly_Sales','MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5'].sum()
df_c_2 = df_raw.groupby(by=['Date','Store'])["IsHoliday","Temperature","Fuel_Price","CPI","Unemployment","Size","TypeA","TypeB","TypeC"].mean()

df_c = pd.concat([df_c_1, df_c_2], axis=1) 
df_c.swaplevel(0, 1, axis=0)
df_c = df_c.reset_index()

df_c

df_c['Date'] = pd.to_datetime(df_c['Date'])

"""Correlation Analysis

*Data combined by store and date*
"""

import seaborn as sns

corr_1 = df_c.iloc[:,2:18].corr()
plt.figure(figsize=(15,8))
sns.heatmap(corr_1, 
            annot=True, fmt=".3f",
            xticklabels=corr_1.columns.values,
            yticklabels=corr_1.columns.values,
            cmap="Blues")
plt.show()

"""*raw data but replaced NAN by genarated data*"""

import seaborn as sns

corr = df[['Weekly_Sales','Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5','Size']].corr()
plt.figure(figsize=(15,10))
sns.heatmap(corr, 
            annot=True, fmt=".3f",
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values,
            cmap="Blues")
plt.show()

"""#Linear Regression"""

df_reg = df_c.drop(df_c[(df_c['MarkDown1']== 0) & (df_c['MarkDown5']== 0) 
& (df_c['MarkDown4']== 0) & (df_c['MarkDown3']== 0) & (df_c['MarkDown2']== 0)].index)

df_reg = df_reg.reset_index()
df_reg = df_reg[['Store','Date','Weekly_Sales','MarkDown1',	'MarkDown2',	'MarkDown3',	'MarkDown4',	'MarkDown5',	'Temperature',	'Fuel_Price',	'CPI',	'Unemployment',	'Size','IsHoliday','TypeA','TypeB','TypeC']]

from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler, RobustScaler

robust_scaler_data = preprocessing.RobustScaler().fit(df_reg.iloc[:,3:13])
stdize = robust_scaler_data.transform(df_reg.iloc[:,3:13])

stdize_df = pd.DataFrame(stdize)
sales = df_reg['Weekly_Sales'] / 1000000  # in million $
df_reg = pd.concat([df_reg[['Store','Date']], sales, stdize_df, df_reg[['IsHoliday',	'TypeA','TypeB','TypeC']]], axis = 1)

from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression

x_li, y_li = df_reg.iloc[:,3:17], df_reg.iloc[:,2:3]

lin_reg = LinearRegression()

mse_li = cross_val_score(lin_reg, x_li, y_li, scoring = 'neg_mean_squared_error', cv=5)
mean_mse_li = np.mean(mse_li)

print(mean_mse_li)

"""#Ridge regression"""

from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import Ridge

ridge = Ridge()

parameters = {'alpha': [1e-15, 1e-10, 1e-8, 1e-4, 1e-3, 1e-2, 1, 5, 10, 20]}

ridge_regressor = GridSearchCV(ridge, parameters, scoring = 'neg_mean_squared_error', cv=5)

ridge_regressor.fit(x_li, y_li)

print(ridge_regressor.best_params_)
print(ridge_regressor.best_score_)

"""#Lasso"""

from sklearn.linear_model import Lasso

lasso = Lasso()

parameters = {'alpha': [1e-15, 1e-10, 1e-8, 1e-4, 1e-3, 1e-2, 1, 5, 10, 20]}

lasso_regressor = GridSearchCV(lasso, parameters, scoring = 'neg_mean_squared_error', cv=5)

lasso_regressor.fit(x_li, y_li)

print(lasso_regressor.best_params_)
print(lasso_regressor.best_score_)

"""#DNN"""

df_dnn = df_c.drop(df_c[(df_c['MarkDown1']== 0) & (df_c['MarkDown5']== 0) 
& (df_c['MarkDown4']== 0) & (df_c['MarkDown3']== 0) & (df_c['MarkDown2']== 0)].index)

df_dnn = df_dnn.reset_index()
df_dnn = df_dnn[['Store','Date','Weekly_Sales','MarkDown1',	'MarkDown2',	'MarkDown3',	'MarkDown4',	'MarkDown5',	'Temperature',	'Fuel_Price',	'CPI',	'Unemployment',	'Size','IsHoliday','TypeA','TypeB','TypeC']]

from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler, RobustScaler

robust_scaler_data = preprocessing.RobustScaler().fit(df_dnn.iloc[:,3:13])
stdize = robust_scaler_data.transform(df_dnn.iloc[:,3:13])

stdize_df = pd.DataFrame(stdize)
sales = df_dnn['Weekly_Sales'] / 1000000  # in million $
df_dnn = pd.concat([df_dnn[['Store','Date']], sales, stdize_df, df_dnn[['IsHoliday',	'TypeA','TypeB','TypeC']]], axis = 1)
# df_dnn

from sklearn.model_selection import train_test_split

x,y = df_dnn.iloc[:,3:17], df_dnn.iloc[:,2:3]

x_train, x_test, y_train, y_test =train_test_split(x, y, test_size=0.2, random_state=42)

import tensorflow as tf
  
dnn = tf.keras.Sequential()
dnn.add(tf.keras.layers.Dense(256, input_shape=(14,), kernel_initializer = 'normal', activation='relu'))
dnn.add(tf.keras.layers.Dense(64, kernel_initializer = 'normal', activation='relu'))
dnn.add(tf.keras.layers.Dense(1, kernel_initializer = 'normal', activation='linear'))
  
dnn.compile(optimizer='adam', loss='mse')

history = dnn.fit(x_train, y_train, validation_data = (x_test, y_test) ,batch_size = 30, epochs = 500, verbose=1)

loss     = history.history[    'loss' ]
val_loss = history.history['val_loss' ]

epochs   = range(len(loss)) # Get number of epochs

plt.plot  ( epochs,     loss )
plt.plot  ( epochs, val_loss )
plt.title ('Training and validation loss'   )

"""#Elasticity Analysis

**Simple Elasticity**
"""

df_e = df_c[(df_c['Temperature'] > 0) & (df_c['MarkDown1'] > 0) & (df_c['MarkDown2'] > 0) & 
            (df_c['MarkDown3'] > 0) & (df_c['MarkDown4'] > 0) & (df_c['MarkDown5'] > 0)]

import math
df_ln = np.log(df_e[['Weekly_Sales','Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'Size',
                   'MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5']])

df_e = pd.concat([df_e[['Date','Store']], df_ln], axis=1) 
df_e = df_e.reset_index()
df_e = df_e.drop('index', axis = 1)
# df_e

from sklearn.linear_model import LinearRegression

X = df_e[['Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'Size',
                   'MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5']]
y = df_e["Weekly_Sales"]

ela_reg = LinearRegression().fit(X, y)

ela_reg.coef_

ela_reg.intercept_

# ela_reg.score(X, y)

"""**IsHoliday Markdown Elasticity**"""

df_ee = df_c[df_c['IsHoliday'] == 1] 
df_ee = df_ee[(df_c['MarkDown1'] > 0) & (df_c['MarkDown2'] > 0) & 
            (df_c['MarkDown3'] > 0) & (df_c['MarkDown4'] > 0) & (df_c['MarkDown5'] > 0)]

import math
df_ln_e = np.log(df_ee[['Weekly_Sales','MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5']])

df_ee = pd.concat([df_ee[['Date','Store']], df_ln_e], axis=1) 
df_ee = df_ee.reset_index()
df_ee = df_ee.drop('index', axis = 1)

from sklearn.linear_model import LinearRegression

X_e = df_ee[['MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5']]
y_e = df_ee["Weekly_Sales"]

ela_reg = LinearRegression().fit(X_e, y_e)

ela_reg.coef_

ela_reg.intercept_

"""**NotHoliday Markdown Elasticity**"""

df_en = df_c[df_c['IsHoliday'] == 0] 
df_en = df_en[(df_c['MarkDown1'] > 0) & (df_c['MarkDown2'] > 0) & 
            (df_c['MarkDown3'] > 0) & (df_c['MarkDown4'] > 0) & (df_c['MarkDown5'] > 0)]

import math
df_ln_n = np.log(df_en[['Weekly_Sales','MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5']])

df_en = pd.concat([df_en[['Date','Store']], df_ln_n], axis=1) 
df_en = df_en.reset_index()
df_en = df_en.drop('index', axis = 1)

from sklearn.linear_model import LinearRegression

X_n = df_en[['MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5']]
y_n = df_en["Weekly_Sales"]

ela_reg = LinearRegression().fit(X_n, y_n)

ela_reg.coef_

ela_reg.intercept_



"""#Prediction"""

!ls /content/drive/'My Drive'/'Retail Analytics'/'forecast_data.csv'

df_future = pd.read_csv('/content/drive/My Drive/Retail Analytics/forecast_data.csv')

df_future = df_future[0:12]
df_future

df_future['date'] = pd.to_datetime(df_future['date'])
df_future = df_future.set_index('date')

robust_scaler_data = preprocessing.RobustScaler().fit(df_future.iloc[:,3:13])
stdize = robust_scaler_data.transform(df_future.iloc[:,3:13])

stdize_future = pd.DataFrame(stdize)
df_future = pd.concat([df_future[['store','date','Weekly_Sales']], stdize_future, df_future[['IsHoliday',	'TypeA','TypeB','TypeC']]], axis = 1)

df_future

future = dnn.predict(df_future.iloc[:,3:17])

df_future['date'] = pd.to_datetime(df_future['date'])
df_future['Weekly_Sales'] = future

df_future[['date','Weekly_Sales']]

plt.figure(figsize = (14,8))
sns.lineplot(df_future['date'],df_future['Weekly_Sales'],color='c')
# plt.ylim(30000000,90000000)

plt.show()
