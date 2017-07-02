# Simply uses the assessors estimate to predict price, so we can see how much better the machine learning models are.
# requires data from Assemble_Data.py

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
from sklearn.linear_model import LinearRegression

# https://stats.stackexchange.com/questions/58391/mean-absolute-percentage-error-mape-in-scikit-learn
def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

working_df = pd.read_csv('Data\\$working_data_5c.csv')

# eliminate some outliers, homes above an estimated value of $2 million are especially difficult to model
# with the available data
working_df = working_df[working_df['Age_Yrs'] > 0]
working_df = working_df[working_df['totalActualVal'] <= 2000000]

y = working_df['price']
columns = working_df.columns[2:]
X = working_df.drop(columns, axis=1)  # , 'totalActualVal'
X = X.drop(labels=['price'], axis=1)
# 70/30 split of data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=245)

# determine metrics
gradient, intercept, r_value, p_value, std_err = stats.linregress(X_test['totalActualVal'], y_test)

print 'Gradient: %.4f' % gradient
print 'R Value: %.4f' % r_value
print 'R-Squared: %.4f' % r_value ** 2

# adjusted R-squared - https://www.easycalculation.com/statistics/learn-adjustedr2.php
r_sq_adj = 1 - ((1 - r_value ** 2) * (len(y_test) - 1) / (len(y_test) - X_train.shape[1] - 1))
print 'R-Squared Adjusted: %.4f' % r_sq_adj

mape = mean_absolute_percentage_error(y_test, X_test['totalActualVal'])
print 'MAPE: %.4f' % mape

# plot with regression lines, one for actual data, one to represent ideal answer
z = np.polyfit(X_test['totalActualVal'], y_test, 1)
print 'z'
print z
y_poly = [z[0] * x + z[1] for x in range(int(intercept), 3100000 + int(intercept), 100000)]
x_poly = [x for x in range(0, 3100000, 100000)]
y_perfect = [x for x in range(0, 3100000, 100000)]

plt.figure(0)
plt.plot(X_test, y_test, ".")
plt.plot(x_poly, y_poly, "-")
plt.plot(x_poly, y_perfect, "-")
plt.xlim(0, 4000000)
plt.ylim(0, 4000000)
plt.xlabel("Est Price")
plt.ylabel("Actual Price")
plt.title("Estimated vs. Actual Sales Price")
plt.show()
plt.close()

# delta_price = pd.Series((X_test['totalActualVal'] / y_test * 100.0) - 100.0)
# delta_price.to_csv('Data\\delta_price_basic.csv', index=False)

print 'min price, actual: %.2f' % np.min(y_test)
print 'min price, assessor estimate: %.2f' % np.min(X_test['totalActualVal'])
