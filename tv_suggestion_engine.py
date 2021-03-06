# coding=utf-8
#based on the follwing tutorial: https://elitedatascience.com/python-machine-learning-tutorial-scikit-learn

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import metrics
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.externals import joblib

dataset_url = 'Dataset.csv'
data = pd.read_csv(dataset_url, sep=';')
data['TV_technology'], unique = pd.factorize(data['TV_technology'])
data['CZ_group5_name'], unique = pd.factorize(data['CZ_group5_name'])
data['TV_product_grouped'], unique = pd.factorize(data['TV_product_grouped'])
data['Household_municipality'], unique = pd.factorize(data['Household_municipality'])
data.fillna(0, inplace=True)

categoryGroup = data[['TV_flow_consump_cat_children', 'TV_flow_consump_cat_documentary',
          'TV_flow_consump_cat_movies', 'TV_flow_consump_cat_leisure',
          'TV_flow_consump_cat_art', 'TV_flow_consump_cat_music',
          'TV_flow_consump_cat_news', 'TV_flow_consump_cat_politics',
          'TV_flow_consump_cat_series', 'TV_flow_consump_cat_show',
          'TV_flow_consump_cat_sports', 'TV_flow_consump_cat_other']]

categories = categoryGroup.idxmax(axis=1)
data['category_num'], uniques = pd.factorize(categories)
print uniques

#data.columns.difference(test.columns) test if test and data has same columns

#print data
# print data.head()
# print data.shape
#print data.describe()

y = data.category_num
# X = data.drop(['TV_flow_consump_cat_children', 'TV_flow_consump_cat_documentary',
#           'TV_flow_consump_cat_movies', 'TV_flow_consump_cat_leisure',
#           'TV_flow_consump_cat_art', 'TV_flow_consump_cat_music',
#           'TV_flow_consump_cat_news', 'TV_flow_consump_cat_politics',
#           'TV_flow_consump_cat_series', 'TV_flow_consump_cat_show',
#           'TV_flow_consump_cat_sports', 'TV_flow_consump_cat_other', 'category_num'], axis=1)
X = data.drop(['category_num'], axis=1)

#divide into test and train sets
# (test_size is the % of the total sample to use for validation,
# random_state makes sure that it is split in the same way, every time it is run with the same number,
# stratify means to make sure that you get a good sample of all the different groups
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.2,
                                                    random_state=123)

# standardize data
# save means and standard deviations, so the standarditation process is the same for the test and train sets
#scaler = preprocessing.StandardScaler().fit(X_train)
#this is done automatically in the crossvalidation pipeline here:
pipeline = make_pipeline(preprocessing.StandardScaler(),
                         RandomForestRegressor(n_estimators=100))

# dtree = DecisionTreeClassifier(criterion='entropy', random_state=0)

#tuning parameters (docs: http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html):
hyperparameters = { 'randomforestregressor__max_features' : ['auto', 'sqrt', 'log2'],
                  'randomforestregressor__max_depth': [None, 5, 3, 1]}

#perform crossvalidation on the set by cutting it into cv chunks and
#validate 1 chunk against the rest, cv times
clf = GridSearchCV(pipeline, hyperparameters, cv=10)
# Fit and tune model
#print X_train
#print y_train
clf.fit(X_train, y_train)

# dtree.fit(X_train, y_train)
#
# export_graphviz(dtree, feature_names=X_train.columns)
# print y_test
# print dtree.predict(X_test)
#
# print metrics.mean_absolute_error(y_test, dtree.predict(X_test))


print clf.best_params_
#print clf.refit

y_pred = clf.predict(X_test)

#print y_pred
#print y_test
#R^2 (coefficient of determination) regression score function.
#Best possible score is 1.0 and it can be negative (because the model can be arbitrarily worse).
# A constant model that always predicts the expected value of y, #
# disregarding the input features, would get a R^2 score of 0.0.
print r2_score(y_test, y_pred)

#The MSE is a measure of the quality of an estimator—it is always non-negative, and values closer to zero are better.
print mean_squared_error(y_test, y_pred)

joblib.dump(clf, 'model.pkl')
