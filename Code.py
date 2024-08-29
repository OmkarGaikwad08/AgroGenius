import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#%%
crop_data = pd.read_csv("dataset.csv")
#%%
crop_data.head()
#%%
crop_data.tail()
#%%
crop_data.info()
#%%
crop_data.isnull().sum()
#%%
fig=plt.figure(figsize=(10,5))
#%%
crop_data["label"].nunique()
#%%
fig= plt.figure(figsize=(24,10))
sns.barplot(data=crop_data, x="label", y="N")
plt.show()
#%%
fig= plt.figure(figsize=(25,7))
sns.lineplot(data=crop_data, x="label", y="N")
plt.show()
#%%
X= crop_data.drop(columns=["label"])
#%%
Y= crop_data["label"]
#%%
X.info()
#%%
Y
#%%
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
#%%
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, random_state=0, test_size=0.3)
#%%
knn= KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, Y_train)
predictions = knn.predict(X_test)
#%%
from sklearn.metrics import confusion_matrix, classification_report
model = print(confusion_matrix(predictions, Y_test))
model
print(classification_report(Y_test, predictions))
#%%
print("ENTER YOUR OWN DATA")
N=int(input("Enter Nitrogen : "))
P=int(input("Enter Phosphorous : "))
K=int(input("Enter Potassium : "))
temp = float(input("Enter temperature : "))
humidity =float(input("Enter humidity : "))
ph=float(input("Enter ph value : "))
rainfall=float(input("Enter rainfall amount : "))

userinput = [N,P,K,temp,humidity,ph,rainfall]

result =knn.predict([userinput])[0]
print(result)
#%%