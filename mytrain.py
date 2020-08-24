import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression





df=pd.read_csv('covidnew.csv')



train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)
# this will print length of test set and train set
print("test data is",len(test_set))
print("train data is",len(train_set))


# for training:seperating features and labels
x_train_feature=train_set.drop(["prob"],axis=1)
y_train_label=train_set["prob"].copy()


# to convert to array
x_train_feature.to_numpy()
y_train_label.to_numpy()

# for testing:seperating features and labels
x_test_feature=test_set.drop(["prob"],axis=1)
y_test_label=test_set["prob"].copy()


x_test_feature.to_numpy()
y_test_label.to_numpy()



# logistic regression
model=LogisticRegression()
# model=DecisionTreeRegressor()
# model=RandomForestRegressor()
# fit function takes label and features
model.fit(x_train_feature,y_train_label)



# open a file, where you ant to store the data
file = open('clf.pkl', 'wb')

# dump model information to that file
pickle.dump(model, file)
file.close()

