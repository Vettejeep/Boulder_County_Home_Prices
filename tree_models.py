# Basic Tree Models to Analyze Boulder County Home Prices vs. Assessor's Data
# Copyright (C) 2017  Kevin Maher

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pandas as pd
import numpy as np
from math import sqrt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from scipy import stats

from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.ensemble import GradientBoostingRegressor, AdaBoostRegressor


working_df = pd.read_csv('Data\\$working_data_other_Areas.csv')

working_df = working_df[working_df['Age_Yrs'] > 0]
working_df = working_df[working_df['totalActualVal'] <= 2000000]

print working_df.head()

if working_df.isnull().any().any():
    print 'WARNING: NA values in dataframe!!!'

# root mean squared error, on log of price - per Kaggle
# https://www.kaggle.com/c/house-prices-advanced-regression-techniques#evaluation
y = np.log(working_df['price'])
X = working_df.drop(labels=['price'], axis=1)  # , 'totalActualVal'

print 'Total Data Points: %d' % len(X.index)
print 'Shape of input data %s: ' % str(X.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=242)

reg = RandomForestRegressor(n_estimators=1000, n_jobs=3, random_state=42)
# reg = RandomForestRegressor(n_estimators=100, criterion='mae', random_state=42)  # crashed, ran slow
# reg = GradientBoostingRegressor(n_estimators=4000)
# reg = AdaBoostRegressor(n_estimators=1000)
# reg = AdaBoostRegressor(base_estimator=RandomForestRegressor(n_estimators=40, random_state=42), n_estimators=1000)
# reg = ExtraTreesRegressor(n_estimators=1000, n_jobs=3)

# scores = cross_val_score(reg, X_train, y_train, cv=10, scoring='neg_mean_squared_error')
# print "Cross Validation RMSE: %.6f" % np.mean(np.sqrt(-scores))

reg.fit(X_train, y_train)
pred = reg.predict(X_test)

rmse = sqrt(mean_squared_error(y_test, pred))

print "Model RMSE on 30%% Test Data: %.6f" % rmse

y_test = np.exp(y_test)
pred = np.exp(pred)

gradient, intercept, r_value, p_value, std_err = stats.linregress(y_test, pred)

print 'Gradient: %.4f' % gradient
print 'R Value: %.4f' % r_value
print 'R-Squared: %.4f' % r_value ** 2

# adjusted R-squared - https://www.easycalculation.com/statistics/learn-adjustedr2.php
r_sq_adj = 1 - ((1 - r_value ** 2) * (len(y_test) - 1) / (len(y_test) - X_train.shape[1] - 1))
print 'R-Squared Adjusted: %.4f' % r_sq_adj

# plt.figure(0)
# plt.plot(y_test, pred, ".")
# plt.xlim(0, 2500000)
# plt.ylim(0, 2500000)
# plt.xlabel("Actual Price")
# plt.ylabel("Est Price")
# plt.title("Estimation of Sales Price")
# plt.show()

# calculate forest feature importance
# importances = reg.feature_importances_
# std = np.std([tree.feature_importances_ for tree in reg.estimators_],
#              axis=0)
#
# imp_df = pd.DataFrame(data=np.column_stack([X_train.columns, importances, std]),
#                       columns=['Feature Name', 'Importance', 'Standard Deviation'])
#
# imp_df.sort_values(by=['Importance'], ascending=False, inplace=True)  # could reset index
# print imp_df.head(12)

print 'Done'

### model with decks, porches, patios, etc.
# RF model with estimators = 100
# Cross Validation RMSE: 0.129623
# Model RMSE on 30% Test Data: 0.125721
# Gradient: 0.9158
# R Value: 0.9604
# R-Squared: 0.9224
# R-Squared Adjusted: 0.9206

# Processing gradient boosting for estimators = 400
# Cross Validation RMSE: 0.126141
# Model RMSE on 30% Test Data: 0.120483
# Gradient: 0.9348
# R Value: 0.9634
# R-Squared: 0.9281
# R-Squared Adjusted: 0.9265

### these are models without decks, porches, patios, etc.
# First RF Model
# Processing for estimators = 100
# Cross Validation RMSE: 0.129967
# Model RMSE on 30% Test Data: 0.124091
# Gradient: 0.9110
# R Value: 0.9597
# R-Squared: 0.9210
# R-Squared Adjusted: 0.9194

# Gradient Boosting - candidate for multi model
# Processing for estimators = 100
# Cross Validation RMSE: 0.130389
# Model RMSE on 30% Test Data: 0.126448
# Gradient: 0.9007
# R Value: 0.9566
# R-Squared: 0.9152
# R-Squared Adjusted: 0.9134

# Processing for estimators = 400
# Cross Validation RMSE: 0.126425
# Model RMSE on 30% Test Data: 0.121064
# Gradient: 0.9259
# R Value: 0.9584
# R-Squared: 0.9186
# R-Squared Adjusted: 0.9169