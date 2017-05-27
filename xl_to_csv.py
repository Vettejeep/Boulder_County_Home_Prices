# Analyze Boulder County Home Prices vs. Assessor's Data, file conversion utility
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

import os
import pandas as pd

list_dir = 'C:\\Users\\Kevin\\PycharmProjects\\MSDS692\\Data\\2016'
# list_dir = 'C:\\Users\\Kevin\\PycharmProjects\\MSDS692\\Data\\2015'
# list_dir = 'C:\\Users\\Kevin\\PycharmProjects\\MSDS692\\Data\\2014'
# list_dir = 'C:\\Users\\Kevin\\PycharmProjects\\MSDS692\\Data\\2013'

files = os.listdir(list_dir)

for f in files:
    try:
        name, ext = f.split('.')
    except ValueError:
        continue

    try:
        if ext == 'xlsx':
            full_xl = os.path.join(list_dir, f)
            df = pd.read_excel(full_xl)
            full_csv = os.path.join(list_dir, name + '.csv')
            df.to_csv(full_csv, encoding='utf8')
            print '%s written to csv' % full_csv
    except:
        print '%s has error' % full_csv