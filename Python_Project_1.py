import requests as rq
import pandas as pd 
import numpy as np

import scipy 
import sklearn 
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from math import * 


htmlRequest = rq.get("https://raw.githubusercontent.com/charvi5/KingCountyHousingData/master/kc_house_data.csv")

with open("export3.txt",mode="w+", encoding="utf8") as f:
    f.write(htmlRequest.text)
House = pd.read_csv("export3.txt", delimiter=',')

#val=len(list(House['date'].head()))
#print(House['date'].head())
for i in range(len(House['date'])): 
     House['date'].set_value(i,int(House['date'][i][0:4]))
      
#print(House['date'].head().astype(int).dtypes)
House['age']=House['date'].astype(int)-House['yr_built']
#dataframe we'll use without zip_code
Houses_price = House[['id','price','bedrooms','bathrooms','sqft_living','sqft_lot','grade','sqft_above','sqft_basement','floors','waterfront','zipcode','age']][House.bedrooms != House['bedrooms'].max()]
#print(len(Houses_price))
for i in range(1,14) :
  if i != 2 :
    Houses_price['Grade'+str(i)]=0
    Houses_price.loc[Houses_price['grade'] == i,'Grade' + str(i) ] = 1
# sorting DataFrame Houses_price
Houses_price = Houses_price.sort_values( by ='zipcode')
# creation of Regions variables and new DataFrame Regions
zip_code = Houses_price['zipcode'][0]
index = 1
li = []
li2=[]

for x in Houses_price['zipcode'] :
  if zip_code != x : 
    li.append(index)
    li2.append(x)
    Houses_price ['Region'+str(index)] = 0
    Houses_price.loc[Houses_price['zipcode'] == x, 'Region'+str(index) ] = 1
    index += 1 
  zip_code = x 

Regions_Data = pd.DataFrame(li2,index=li,columns=['Regions'])
#print(Regions_Data)
#sample of data + header
#print(Houses_price.head(20), Houses_price.columns)
#for x in Houses_price.columns : 
#print(Houses_price[x].describe())

# regression (spliting data into test and training sets)
L=Houses_price.drop(['id','price','sqft_living','sqft_above','grade','zipcode'],axis=1)
for i in range(1,index) : 
    Houses_price['Region'+str(i)+'_bdedrooms_bathrooms']= Houses_price['bedrooms']*Houses_price['Region'+str(i)]*Houses_price['bathrooms']
x=Houses_price.drop(['id','price','sqft_living','sqft_above','grade','zipcode'],axis=1)

#x=Houses_price.drop(['id','price','sqft_living','sqft_above','grade','zipcode'],axis=1)
y1=Houses_price['price']
y=Houses_price['price']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.0154,random_state = 1)  
L_train, L_test, y1_train, y1_test = train_test_split(L, y1, test_size=0.0154, random_state = 1)  
#x_train=np.mat(sm.add_constant(x_train))
model = sm.OLS(y_train,x_train,hasconst=None).fit(cov_type='HC1')
#print(model.summary())
##calculation: (X.T*X).I*X.T*y
#XprimeX=X.T*X
#XprimeXinv=XprimeX.I
#XprimeY=X.T*y
#betahat=XprimeXinv*XprimeY
L = StandardScaler().fit_transform(L_train)
pca = PCA()  
L_train = pca.fit_transform(L)
#print(pca.explained_variance_ratio_)
#print(pca.explained_variance_ratio_)
#X_train=np.mat(sm.add_constant(X_train))
model1 = sm.OLS(y1_train,L_train).fit(cov_type='HC1')
#print(model1.summary())

#print(x_test)
#print(y_test)

# forecasting with model
beta =model.params
def prediction_model(bedrooms, bathrooms, sqft_lot, sqft_basement, floors, waterfront, age, grade, zip_code):
  bedrooms = eval(bedrooms)
  bathrooms = eval(bathrooms)
  sqft_lot = eval(sqft_lot)
  sqft_basement = eval(sqft_basement)
  floors = eval(floors)
  waterfront = eval(waterfront)
  age = eval(age)
  grade = eval(grade) 
  zip_code= eval(zip_code) 

  Fo = model.predict(x_test)

  if zip_code!=0 : 
     al = Regions_Data[Regions_Data.Regions == zip_code].index
     if grade != 1 :
          forecast = beta[0]*bedrooms + beta[1]*bathrooms + beta[2]*sqft_lot + beta[3]*sqft_basement+beta[4]*floors+beta[5]*waterfront+beta[6]*age+ beta[5+grade]+beta[18+al[0]]+beta[88+al[0]]*bedrooms*bathrooms
     else :
          forecast = beta[0]*bedrooms + beta[1]*bathrooms + beta[2]*sqft_lot + beta[3]*sqft_basement+beta[4]*floors+beta[5]*waterfront+beta[6]*age+ beta[6+grade]+beta[18+al[0]]+beta[88+al[0]]*bedrooms*bathrooms
  else :
      if grade != 1 :
          forecast = beta[0]*bedrooms + beta[1]*bathrooms + beta[2]*sqft_lot + beta[3]*sqft_basement+beta[4]*floors+beta[5]*waterfront+beta[6]*age+ beta[5+grade]
      else :
          forecast = beta[0]*bedrooms + beta[1]*bathrooms + beta[2]*sqft_lot + beta[3]*sqft_basement+beta[4]*floors+beta[5]*waterfront+beta[6]*age+ beta[6+grade] 
  return forecast
  # #calculation of RMSE
  # RMSE_ = (Fo-y_test)*(Fo-y_test)
  # RMSE = 0 
  # for i in y_test.index : 
  #      RMSE = RMSE+RMSE_[i]

  # return "<script> alert({}, {});</script>".format(sqrt(RMSE/len(y_test))/469036,1092)