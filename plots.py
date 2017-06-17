# Plotting routines in Python
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
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

working_df = pd.read_csv('Data\\$working_data_5c.csv')

working_df = working_df[working_df['Age_Yrs'] > 0]
working_df = working_df[working_df['totalActualVal'] <= 2000000]

# y = working_df['price']
# X = working_df.drop(labels=['price'], axis=1)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=245)

# x_val = X_test['TotalFinishedSF']
# y_price = y_test
#
# print 'Max, X axis: %.2f' % np.max(x_val)
# print 'Min, X axis: %.2f' % np.min(x_val)
#
# plt.figure(0)
# plt.plot(x_val, y_price, ".")
# plt.xlim(0, 7000)
# plt.ylim(0, 3500000)
# plt.xlabel("Home Sq. Ft.")
# plt.ylabel("Sales Price")
# plt.title("Finished Sq. Ft. to Sales Price")
# plt.show()
# plt.close()

# x_val = X_test['GIS_sqft']
# y_price = y_test
#
# print 'Max, X axis: %.2f' % np.max(x_val)
# print 'Min, X axis: %.2f' % np.min(x_val)
#
# plt.figure(0)
# plt.plot(x_val, y_price, ".")
# plt.xlim(0, 100000)
# plt.ylim(0, 3500000)
# plt.xlabel("Lot Size, Sq. Ft.")
# plt.ylabel("Sales Price")
# plt.title("Lot Size vs. Sales Price")
# plt.show()
# plt.close()

Age_Median_Price = working_df['price'].groupby(working_df['Age_Yrs']).median()
Age_Median_Price = Age_Median_Price[:60]
print Age_Median_Price
age = [x for x in range(1, 61)]

# plt.figure(0)
# plt.plot(age, Age_Median_Price, "-")
# plt.xlim(0, 60)
# plt.ylim(0, 800000)
# plt.xlabel("Age, years")
# plt.ylabel("Median Sales Price")
# plt.title("Age vs. Median Sales Price")
# plt.show()
# plt.close()

Age_Count = working_df['price'].groupby(working_df['Age_Yrs']).count()
print Age_Count
Age_Count = Age_Count[:60]

# plt.figure(1)
# plt.plot(age, Age_Count, "-")
# plt.xlim(0, 60)
# plt.ylim(0, 500)
# plt.xlabel("Age, years")
# plt.ylabel("Count of Sales")
# plt.title("Age vs. Count of Sales")
# plt.show()
# plt.close()

median_home_size_by_year = working_df['TotalFinishedSF'].groupby(working_df['Age_Yrs']).median()
median_home_size_by_year = median_home_size_by_year[:60]

# plt.figure(2)
# plt.plot(age, median_home_size_by_year, "-")
# plt.xlim(0, 60)
# plt.ylim(0, 3000)
# plt.xlabel("Age, years")
# plt.ylabel("Median Home SF")
# plt.title("Age vs. Median Home SF")
# plt.show()
# plt.close()
#
print np.median(working_df['TotalFinishedSF'])
print min(working_df['TotalFinishedSF'])

# effective age in years
Age_Median_Price = working_df['price'].groupby(working_df['Effective_Age_Yrs']).median()
Age_Median_Price = Age_Median_Price[:60]
print Age_Median_Price
age = [x for x in range(1, 61)]

# plt.figure(3)
# plt.plot(age, Age_Median_Price, "-")
# plt.xlim(0, 60)
# plt.ylim(0, 800000)
# plt.xlabel("Effective Age, years")
# plt.ylabel("Median Sales Price")
# plt.title("Effective Age vs. Median Sales Price")
# plt.show()
# plt.close()

# main floor sf
main_floor_sf = working_df['mainfloorSF']
price = working_df['price']

# plt.figure(4)
# plt.plot(main_floor_sf, price, ".")
# plt.xlim(0, 6000)
# plt.ylim(0, 3500000)
# plt.xlabel("Main Floor, Sq. Ft.")
# plt.ylabel("Sales Price")
# plt.title("Main Floor Sq. Ft. vs. Sales Price")
# plt.show()
# plt.close()

# basement sf
# basement_sf = working_df['bsmtSF']
# price = working_df['price']
#
# plt.figure(5)
# plt.plot(basement_sf, price, ".")
# plt.xlim(0, 5000)
# plt.ylim(0, 3500000)
# plt.xlabel("Basement, Sq. Ft.")
# plt.ylabel("Sales Price")
# plt.title("Basement Sq. Ft. vs. Sales Price")
# plt.show()
# plt.close()