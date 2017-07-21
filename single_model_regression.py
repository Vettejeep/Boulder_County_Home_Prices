# Individual Models to Analyze Boulder County Home Prices vs. Assessor's Data

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
from sklearn.preprocessing import StandardScaler
from scipy import stats

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import BayesianRidge
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import Perceptron
from sklearn.linear_model import HuberRegressor
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.ensemble import GradientBoostingRegressor, AdaBoostRegressor
# import xgboost as xgb

# https://stats.stackexchange.com/questions/58391/mean-absolute-percentage-error-mape-in-scikit-learn
def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


# run function solves problems with multi-core usage in cross validation
def run():
    working_df = pd.read_csv('Data\\$working_data_5c.csv')

    # eliminate some outliers, homes above an estimated value of $2 million are especially difficult to model
    # with the available data
    working_df = working_df[working_df['Age_Yrs'] > 0]
    working_df = working_df[working_df['totalActualVal'] <= 2000000]
    # working_df['totalActualVal_Sq'] = working_df['totalActualVal'] ** 2

    print working_df.head()

    # root mean squared error, on log of price - per Kaggle
    # https://www.kaggle.com/c/house-prices-advanced-regression-techniques#evaluation
    y = np.log(working_df['price'])
    X = working_df.drop(labels=['price'], axis=1)  # , 'totalActualVal'

    # 70/30 split of data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=245)

    # only needed for some regressors, generally not required by tree methods and
    # has a minimal effect upon linear regression, use for SVR and MLP
    # sc = StandardScaler()
    # sc.fit(X_train)
    # X_train = sc.transform(X_train)
    # X_test = sc.transform(X_test)

    # comment/uncomment to try different regressors
    reg = LinearRegression()
    # reg = Lasso(alpha=0.01, max_iter=5000)
    # reg = BayesianRidge(n_iter=1000)
    # reg = SVR()  # modest performance
    # reg = MLPRegressor(hidden_layer_sizes=(300, 50), activation='logistic', max_iter=20000)  # slow, OK accuracy
    # reg = Perceptron(n_iter=500)  # crashes
    # reg = HuberRegressor(epsilon=5, max_iter=1000)  # mediocre performance
    # reg = RandomForestRegressor(n_estimators=1000, n_jobs=3, random_state=42)
    # reg = GradientBoostingRegressor(learning_rate=0.02,
    #                                             n_estimators=2000,
    #                                             max_depth=6,
    #                                             subsample=0.6,
    #                                             max_features='auto',
    #                                             random_state=42)
    # reg = ExtraTreesRegressor(n_estimators=1000, n_jobs=3)
    # reg = xgb.XGBRegressor(learning_rate=0.075,
    #                                 max_depth=6,
    #                                 min_child_weight=1.0,
    #                                 subsample=1.0,
    #                                 colsample_bytree=0.4,
    #                                 colsample_bylevel=0.8,
    #                                 reg_lambda=1.0,
    #                                 reg_alpha=0,
    #                                 gamma=0,
    #                                 n_estimators=700,
    #                                 seed=42,
    #                                 silent=1)

    print 'Start CV'
    scores = cross_val_score(reg, X_train, y_train, cv=10, scoring='neg_mean_squared_error', n_jobs=-1)
    print "Cross Validation RMSE: %.6f" % np.mean(np.sqrt(-scores))

    print 'Start Training'
    reg.fit(X_train, y_train)
    pred = reg.predict(X_test)

    rmse = sqrt(mean_squared_error(y_test, pred))
    print "Model RMSE on 30%% Test Data: %.6f" % rmse

    gradient, intercept, r_value, p_value, std_err = stats.linregress(np.exp(pred), np.exp(y_test))
    print 'Gradient: %.4f' % gradient
    print 'R Value: %.4f' % r_value
    print 'R-Squared: %.4f' % r_value ** 2

    # adjusted R-squared - https://www.easycalculation.com/statistics/learn-adjustedr2.php
    r_sq_adj = 1 - ((1 - r_value ** 2) * (len(y_test) - 1) / (len(y_test) - X_train.shape[1] - 1))
    print 'R-Squared Adjusted: %.4f' % r_sq_adj

    mape = mean_absolute_percentage_error(np.exp(y_test), np.exp(pred))
    print 'MAPE: %.4f' % mape

    print 'Done'

if __name__ == '__main__':
    run()
