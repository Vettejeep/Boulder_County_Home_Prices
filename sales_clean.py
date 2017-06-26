# Data Pre-processor to Analyze Boulder County Home Prices vs. Assessor's Data
# Creates a cleaned sales file for use by the assemble data script
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
# sharing the data and implied that they charge comercial entities for the data.
# The data has been pre-processed from xlsx to csv files because OpenOffice had
# problems with the xlsx files.

import pandas as pd

# get rid of mobile homes and not arms length transactions
df = pd.read_csv('Data\\2013_2016_Sales.csv')
df['strap'] = df['strap'].apply(lambda x: x.rstrip())
df['Real_Prop'] = df['strap'].apply(lambda x: 1 if x[0] == 'R' else 0)
df = df[df['Real_Prop'] == 1]  # homes are real property, strip out other sales
df = df[df['sales_cd'] == 'Q']  # 'Q' is believed to be arms length transaction per the assessor

df.reset_index(drop=True, inplace=True)
print 'Length: %d' % len(df.index)

# strip out year and month
df['Year'] = df['Tdate'].apply(lambda x: int(x[1:5]))
df['Month'] = df['Tdate'].apply(lambda x: int(x[6:8]))

df.drop(['deedNum', 'Tdate', 'sales_cd', 'status_cd', 'Real_Prop'], axis=1, inplace=True)
df.to_csv('Data\\2013_2016_Sales_Clean.csv')


# df = df[df['Year'] > 2014]
# df.to_csv('Data\\2015_2016_Sales_Clean.csv')


