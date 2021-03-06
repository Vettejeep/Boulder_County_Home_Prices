# Model to Analyze Boulder County Home Prices vs. Assessor's Data
# Produces a blended model, currently best with extra Trees, Gradient Boosting and XG Boost
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

# Data for this project may be the property of the Boulder County Assessor's office,
# they gave me free access as a student but were not clear about any restrictions regarding
# sharing the URL from which the data was downloaded.
# The data has been pre-processed from xlsx to csv files because OpenOffice had
# problems with the xlsx files.
# Data was pre-processed by a data setup script, Assemble_Data.py which produced the
# file '$working_data_5c.csv'

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
import xgboost as xgb
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import Perceptron

# https://stats.stackexchange.com/questions/58391/mean-absolute-percentage-error-mape-in-scikit-learn
def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


working_df = pd.read_csv('Data\\$working_data_5c.csv')

# eliminate some outliers, homes above an estimated value of $2 million are especially difficult to model
# with the available data
working_df = working_df[working_df['Age_Yrs'] > 0]
working_df = working_df[working_df['totalActualVal'] <= 2000000]
working_df.drop('totalActualVal', axis=1, inplace=True)

print working_df.head()

if working_df.isnull().any().any():
    print 'WARNING: NA values in dataframe!!!'

# root mean squared error, on log of price - per Kaggle
# https://www.kaggle.com/c/house-prices-advanced-regression-techniques#evaluation
y = np.log(working_df['price'])
X = working_df.drop(labels=['price'], axis=1)  # , 'totalActualVal'

print 'Total Data Points: %d' % len(X.index)
print 'Shape of input data %s: ' % str(X.shape)

# 70/30 split of data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=245)

# reg1 = RandomForestRegressor(n_estimators=1000, n_jobs=3, random_state=42)
reg2 = GradientBoostingRegressor(learning_rate=0.02,
                                            n_estimators=2000,
                                            max_depth=6,
                                            subsample=0.6,
                                            max_features='auto',
                                            random_state=42)
reg3 = ExtraTreesRegressor(n_estimators=1000, n_jobs=3)
reg4 = xgb.XGBRegressor(learning_rate=0.075,
                                max_depth=6,
                                min_child_weight=1.0,
                                subsample=1.0,
                                colsample_bytree=0.4,
                                colsample_bylevel=0.8,
                                reg_lambda=1.0,
                                reg_alpha=0,
                                gamma=0,
                                n_estimators=700,
                                seed=42,
                                silent=1)

# random forest not used in final model, gradient boosting, extra trees, xg boost in final model
regs = (reg2, reg3, reg4)
preds = np.zeros(shape=(len(y_test), len(regs)))

# analyze each individual model
for i, reg in enumerate(regs):
    print 'Run #%d, %s' % (i+1, str(type(reg)))
    reg.fit(X_train, y_train)
    pred = reg.predict(X_test)
    gradient, intercept, r_value, p_value, std_err = stats.linregress(np.exp(pred), np.exp(y_test))
    print 'Gradient, pred: %.4f' % gradient
    print 'R Value, pred: %.4f' % r_value
    print 'R-Squared, pred: %.4f' % r_value ** 2
    rmse = sqrt(mean_squared_error(y_test, pred))
    print "Model RMSE on 30%% Test Data, pred1: %.6f" % rmse
    r_sq_adj = 1 - ((1 - r_value ** 2) * (len(y_test) - 1) / (len(y_test) - X_train.shape[1] - 1))
    print 'R-Squared Adjusted: %.4f' % r_sq_adj
    mape = mean_absolute_percentage_error(np.exp(y_test), np.exp(pred))
    print 'MAPE: %.4f' % mape

    preds[:, i] = pred

print 'Analyze Blended Model'
pred = np.mean(preds, axis=1)
rmse = sqrt(mean_squared_error(y_test, pred))
print "Blended Model RMSE on 30%% Test Data: %.6f" % rmse
gradient, intercept, r_value, p_value, std_err = stats.linregress(np.exp(pred), np.exp(y_test))
print 'Blended Gradient: %.4f' % gradient
print 'Blended Intercept: %.4f' % intercept
print 'Blended R Value: %.4f' % r_value
print 'Blended R-Squared: %.4f' % r_value ** 2
r_sq_adj = 1 - ((1 - r_value ** 2) * (len(y_test) - 1) / (len(y_test) - X_train.shape[1] - 1))
print 'R-Squared Adjusted: %.4f' % r_sq_adj
mape = mean_absolute_percentage_error(np.exp(y_test), np.exp(pred))
print 'MAPE: %.4f' % mape

# plot with linear regression lines, one for actual data, one to represent ideal answer
z = np.polyfit(np.exp(pred), np.exp(y_test), 1)
print 'z'
print z
y_poly = [z[0] * x + z[1] for x in range(int(intercept), 3600000 + int(intercept), 100000)]
x_poly = [x for x in range(0, 3600000, 100000)]
y_perfect = [x for x in range(0, 3600000, 100000)]

plt.figure(0)
plt.plot(np.exp(pred), np.exp(y_test), ".")
plt.plot(x_poly, y_poly, "-")
plt.plot(x_poly, y_perfect, "-")
plt.xlim(0, 3500000)
plt.ylim(0, 3500000)
plt.xlabel("Est Price")
plt.ylabel("Actual Price")
plt.title("Estimation of Sales Price")
plt.show()
plt.close()

print 'Done'
