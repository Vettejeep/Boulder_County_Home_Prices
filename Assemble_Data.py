# Data Pre-processor to Analyze Boulder County Home Prices vs. Assessor's Data
# Creates the working data frame with numeric and dummy variables

# requires data from sales_clean.py

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
# sharing the data and implied that they  charge comercial entities for the data.
# The data has been pre-processed from xlsx to csv files because OpenOffice had
# problems with the xlsx files.

import pandas as pd
import numpy as np

# read sales data, tells which homes sold in a given year
YEARS = ['2013', '2014', '2015', '2016']
sales_df = pd.read_csv('Data\\2013_2016_Sales_Clean.csv')

# merge tables for assessed values, land, building, addresses
for i, year in enumerate(YEARS):
    print 'Sales Year: %s' % year
    sales_year_df = sales_df[sales_df['Year'] == int(year)]

    #  merge in assessed values
    f = 'Data\\{0}\\{0}_Values.csv'.format(year)
    value_df = pd.read_csv(f)
    value_df.drop(['status_cd'], axis=1, inplace=True)
    value_df['strap'] = value_df['strap'].apply(lambda x: x.rstrip())
    print 'value shape'
    print value_df.shape
    data_df = pd.merge(sales_year_df, value_df, how='inner', on=['strap'], suffixes=('_sales', '_values'))

    # merge in land
    f = 'Data\\{0}\\{0}_Land.csv'.format(year)
    land_df = pd.read_csv(f)
    land_df.drop(['status_cd'], axis=1, inplace=True)
    land_df['strap'] = land_df['strap'].apply(lambda x: x.rstrip())
    print 'land shape'
    print land_df.shape
    data_df = pd.merge(data_df, land_df, how='inner', on=['strap'], suffixes=('_sales', '_land'))

    # merge in primary building for the property
    f = 'Data\\{0}\\{0}_Buildings.csv'.format(year)
    bldg_df = pd.read_csv(f)
    bldg_df.drop(['status_cd'], axis=1, inplace=True)
    bldg_df['strap'] = bldg_df['strap'].apply(lambda x: x.rstrip())

    try:
        bldg_df.drop(['UnitCount'], axis=1, inplace=True)  # fix issue where not all tables have this balue
    except:
        pass

    bldg_df = bldg_df[bldg_df['bld_num'] == 1]
    data_df = pd.merge(data_df, bldg_df, how='inner', on=['strap'], suffixes=('_sales', '_bldg'))
    print 'bldg shape'
    print bldg_df.shape
    data_df.drop_duplicates(subset=['strap', 'Year', 'Month'], keep='first', inplace=True)

    # merge in owner addresses for property city / unincorporated - need better location info
    f = 'Data\\{0}\\{0}_OwnerAddress.csv'.format(year)
    addr_df = pd.read_csv(f)
    addr_df = pd.DataFrame(addr_df.loc[:, ['strap', 'city']])
    addr_df['strap'] = addr_df['strap'].apply(lambda x: x.rstrip())
    print 'addr shape'
    print addr_df.shape
    data_df = pd.merge(data_df, addr_df, how='inner', on=['strap'], suffixes=('_sales', '_addr'))

    if i == 0:
        all_data_df = data_df
    else:
        print 'merge shapes'
        print data_df.shape
        print all_data_df.shape
        all_data_df = all_data_df.append(data_df)

print all_data_df.tail()

del value_df
del land_df
del bldg_df
del addr_df

# keep only single family homes
all_data_df = all_data_df[all_data_df['landClassDscr'] == 'SINGLE FAM.RES.-LAND']
all_data_df = all_data_df[all_data_df['bldgClassDscr'] == 'SINGLE FAM RES IMPROVEMENTS']

print all_data_df['designCodeDscr'].unique()

# home_styles, leaving out condos, townhomes, model gets too big for computing resources
home_styles = ['2 - 3 STORY',
               '1 STORY - RANCH',
               '1920-1939 STYLE',
               'SPLIT LEVEL',
               'BI-LEVEL',
               'A-FRAME',
               '1910-1919 MULTI-STORY STYLE',
               'PRIOR TO 1910 MULTI-STY STYLE',
               '1940-1949 MULTI STORY STYLE',
               '1910-1919 1 STORY STYLE']

# home_styles = ['1 STORY - RANCH', '2 - 3 STORY', 'A-FRAME', 'BI-LEVEL',
#                'PATIO HOMES', 'SPLIT LEVEL']  # , '1 STORY- TOWNHOUSE', 'MULTI STORY- TOWNHOUSE', 'PAIRED HOMES',
all_data_df = all_data_df[all_data_df['designCodeDscr'].isin(home_styles)]

# keep only common deed types
# http://stackoverflow.com/questions/17071871/select-rows-from-a-dataframe-based-on-values-in-a-column-in-pandas
all_data_df['deed_type'] = all_data_df['deed_type'].apply(lambda x: x.strip())
common_deed_types = ['RD', 'RJ', 'SJ', 'SW', 'WD', 'WJ']
all_data_df = all_data_df[all_data_df['deed_type'].isin(common_deed_types)]

# drop rows that have odd values
all_data_df = all_data_df[all_data_df['CompCode'] == 1]  # only a few incomplete homes so drop them?
all_data_df = all_data_df[all_data_df['nbrRoomsNobath'] <= 25]  # 1 outlier with 80+ rooms
all_data_df = all_data_df[all_data_df['city'] != 'BROOMFIELD']  # city is mostly outside Boulder Cty, only 3
all_data_df = all_data_df[all_data_df['city'] != 'GOLDEN']  # city is mostly outside Boulder Cty, only 1

# all_data_df.to_csv('Data\\$all_data_df5c.csv')

# add info from other areas table, decke. porches, patios, etc.
all_data_df['Has_Deck'] = 0
all_data_df['Deck_Area'] = 0
all_data_df['Has_Encl_Porch'] = 0
all_data_df['Encl_Porch_Area'] = 0
all_data_df['Has_Patio'] = 0
all_data_df['Patio_Area'] = 0
all_data_df['Has_Porch'] = 0
all_data_df['Porch_Area'] = 0
all_data_df['Has_Other_Area'] = 0
all_data_df['Other_Area'] = 0

all_data_df.sort_values(by=['Year', 'Month'], inplace=True)
all_data_df.reset_index(drop=True, inplace=True)


class AreaItem:
    def __init__(self, at, aa):
        self.area_type = at
        self.area_area = aa

year = 0
area_dict = {}
total_to_process = len(all_data_df.index)

# merge in other areas table, runs slow, needs to create large dictionary
# doing this without the dictionary looked like it would take many days to run
# sort the data first by year or else wast much time re-building dictionaries for each year
for i in all_data_df.index:
    new_year = all_data_df.loc[i, 'Year']
    strap = all_data_df.loc[i, 'strap']

    if i % 100 == 0:
        print 'Processing %d of other areas for %s (total to do: %d)' % (i, strap, total_to_process)

    # if i == 100:
    #     all_data_df.to_csv('test_100_v2.csv')
    #     print 'Saved first 100 to csv'

    # build the dict for the other areas file, this will allow for matching multiple areas with a home
    # warning: this step takes a while to process
    if year != new_year:
        print 'Processing dict for year: %d; this will take a while' % new_year
        year = new_year

        area_file = 'Data\\{0}\\{0}_OtherAreas.csv'.format(year)
        temp_area_file_df = pd.read_csv(area_file)

        for j in temp_area_file_df.index:
            key = temp_area_file_df.loc[j, 'strap'].rstrip()
            area_type = temp_area_file_df.loc[j, 'SubareaDscr']
            area_area = temp_area_file_df.loc[j, 'ActualArea']
            value = AreaItem(area_type, area_area)

            if key not in area_dict:
                area_dict[key] = [value]
            else:
                area_dict[key].append(value)

        del temp_area_file_df

    # using += handles multiple decks, patios, multiple other areas
    try:
        home_areas = area_dict[strap]

        for area in home_areas:
            if area.area_type == 'DECK AREA':
                all_data_df.loc[i, 'Has_Deck'] = 1
                all_data_df.loc[i, 'Deck_Area'] += area.area_area
            elif area.area_type == 'ENCLOSED PORCH AREA':
                all_data_df.loc[i, 'Has_Encl_Porch'] = 1
                all_data_df.loc[i, 'Encl_Porch_Area'] += area.area_area
            elif area.area_type == 'PATIO AREA':
                all_data_df.loc[i, 'Has_Patio'] = 1
                all_data_df.loc[i, 'Patio_Area'] += area.area_area
            elif area.area_type == 'PORCH AREA':
                all_data_df.loc[i, 'Has_Porch'] = 1
                all_data_df.loc[i, 'Porch_Area'] += area.area_area
            else:
                all_data_df.loc[i, 'Has_Other_Area'] = 1
                all_data_df.loc[i, 'Other_Area'] += area.area_area

    except:
        pass

del area_dict

# drop columns that duplicate others or have little data
drop_cols = ['xfActualVal', 'landAssessedVal', 'bldAssessedVal', 'xfAssessedVal', 'totalAssessedVal', 'landUnitValue',
             'landUnitType', 'landClass', 'landClassDscr', 'GIS_acreage', 'bld_num', 'section_num', 'qualityCodeDscr',
             'bldgClass', 'bldgClassDscr', 'Stories', 'UnitCount']
all_data_df.drop(drop_cols, axis=1, inplace=True)

all_data_df.sort_values(by='price', inplace=True)
all_data_df.reset_index(drop=True, inplace=True)

print all_data_df.head()
print 'Number of Data Points: %d' % len(all_data_df.index)

# all_data_df.to_csv('Data\\$bc_housing_2013_2016_5c.csv')

print all_data_df['deed_type'].unique()
print all_data_df['price'].describe()

# start some data conversions, take numerics first, along with already processed other area data
working_df = all_data_df.loc[:, ['price',
                        'totalActualVal', 'GIS_sqft', 'bsmtSF', 'carStorageSF',
                        'nbrBedRoom', 'nbrRoomsNobath', 'mainfloorSF', 'nbrThreeQtrBaths', 'nbrFullBaths',
                        'nbrHalfBaths', 'TotalFinishedSF',
                        'Has_Deck', 'Deck_Area', 'Has_Encl_Porch', 'Encl_Porch_Area', 'Has_Patio', 'Patio_Area',
                        'Has_Porch', 'Porch_Area', 'Has_Other_Area', 'Other_Area']]
print working_df.head()

working_df.loc[:, 'Time_Period'] = ((all_data_df['Year'] - int(YEARS[0])) * 12) + all_data_df['Month']
working_df.loc[:, 'Age_Yrs'] = all_data_df['Year'] - all_data_df['builtYear']
working_df.loc[:, 'Effective_Age_Yrs'] = all_data_df['Year'] - all_data_df['EffectiveYear']


# converts and joins dummy variables to the model
# source df should not equal dest df or else the categorical features remain in the model along with the dummies
def get_dummies(source_df, dest_df, col, join=True, drop=None):
    dummies = pd.get_dummies(source_df[col], prefix=col)

    print 'Quantities for %s column' % col
    for col in dummies:
        print '%s: %d' % (col, np.sum(dummies[col]))
    print

    if drop is not None:
        dummies.drop([drop], inplace=True)

    if join:
        dest_df = dest_df.join(dummies)
    return dest_df

print 'deed_type'
print all_data_df['deed_type'].describe()
working_df = get_dummies(all_data_df, working_df, 'deed_type')

print 'designCodeDscr'
print all_data_df['designCodeDscr'].describe()
get_dummies(all_data_df, working_df, 'designCodeDscr', join=False)
all_data_df['designCodeDscr'] = all_data_df['designCodeDscr'].apply(lambda x: 'ONE_STORY' if x == '1 STORY - RANCH' else x)
all_data_df['designCodeDscr'] = all_data_df['designCodeDscr'].apply(lambda x: 'ONE_STORY' if x == '1910-1919 1 STORY STYLE' else x)
all_data_df['designCodeDscr'] = all_data_df['designCodeDscr'].apply(lambda x: 'MULTI_STORY' if x == '1910-1919 MULTI-STORY STYLE' else x)
all_data_df['designCodeDscr'] = all_data_df['designCodeDscr'].apply(lambda x: 'ONE_STORY' if x == '1920-1939 STYLE' else x)
all_data_df['designCodeDscr'] = all_data_df['designCodeDscr'].apply(lambda x: 'MULTI_STORY' if x == '1940-1949 MULTI STORY STYLE' else x)
all_data_df['designCodeDscr'] = all_data_df['designCodeDscr'].apply(lambda x: 'MULTI_STORY' if x == '2 - 3 STORY' else x)
all_data_df['designCodeDscr'] = all_data_df['designCodeDscr'].apply(lambda x: 'A-FRAME' if x == 'A-FRAME' else x)
all_data_df['designCodeDscr'] = all_data_df['designCodeDscr'].apply(lambda x: 'BI_LEVEL' if x == 'BI-LEVEL' else x)
all_data_df['designCodeDscr'] = all_data_df['designCodeDscr'].apply(lambda x: 'MULTI_STORY' if x == 'PRIOR TO 1910 MULTI-STY STYLE' else x)
all_data_df['designCodeDscr'] = all_data_df['designCodeDscr'].apply(lambda x: 'BI_LEVEL' if x == 'SPLIT LEVEL' else x)
working_df = get_dummies(all_data_df, working_df, 'designCodeDscr')

print all_data_df['qualityCode'].describe()
get_dummies(all_data_df, working_df, 'qualityCode', join=False)
all_data_df['qualityCode'] = all_data_df['qualityCode'].apply(lambda x: int(x) / 10)
all_data_df['qualityCode'] = all_data_df['qualityCode'].apply(lambda x: x if x >= 3 else 2)
all_data_df['qualityCode'] = all_data_df['qualityCode'].apply(lambda x: x if x <= 6 else 7)
working_df = get_dummies(all_data_df, working_df, 'qualityCode')

working_df['Is_Frame_Const'] = all_data_df['ConstCodeDscr'].apply(lambda x: 1 if x == 'FRAME' else 0)

# LGU -> BGU, LWF -> BWF, LWU -> BWU because too few to use
print all_data_df['bsmtType'].describe()
get_dummies(all_data_df, working_df, 'bsmtType', join=False)
all_data_df['bsmtType'] = all_data_df['bsmtType'].apply(lambda x: str(x).rstrip())
all_data_df['bsmtType'] = all_data_df['bsmtType'].apply(lambda x: 'BGU' if x == 'LGU' else x)
all_data_df['bsmtType'] = all_data_df['bsmtType'].apply(lambda x: 'BWF' if x == 'LWF' else x)
all_data_df['bsmtType'] = all_data_df['bsmtType'].apply(lambda x: 'BWU' if x == 'LWU' else x)
working_df = get_dummies(all_data_df, working_df, 'bsmtType')

# GRF, GRW -> GRA because too few to use
print all_data_df['carStorageType'].describe()
get_dummies(all_data_df, working_df, 'carStorageType', join=False)
all_data_df['carStorageType'] = all_data_df['carStorageType'].apply(lambda x: str(x).rstrip())
all_data_df['carStorageType'] = all_data_df['carStorageType'].apply(lambda x: 'GRA' if x == 'GRF' or x == 'GRW' else x)
working_df = get_dummies(all_data_df, working_df, 'carStorageType')

print all_data_df['AcDscr'].describe()
get_dummies(all_data_df, working_df, 'AcDscr', join=False)
all_data_df['AcDscr'] = all_data_df['AcDscr'].apply(lambda x: str(x).strip())
all_data_df['AcDscr'] = all_data_df['AcDscr'].apply(lambda x: 'NONE' if type(x) != str else x)
all_data_df['AcDscr'] = all_data_df['AcDscr'].apply(lambda x: 'NONE' if x == 'nan' or x == 'ATTIC FAN' else x)
all_data_df['AcDscr'] = all_data_df['AcDscr'].apply(lambda x: 'WHOLE HOUSE' if x == 'YES' else x)
working_df = get_dummies(all_data_df, working_df, 'AcDscr')

print all_data_df['HeatingDscr'].describe()
get_dummies(all_data_df, working_df, 'HeatingDscr', join=False)
all_data_df['HeatingDscr'] = all_data_df['HeatingDscr'].apply(lambda x: str(x).strip())
all_data_df['HeatingDscr'] = all_data_df['HeatingDscr'].apply(lambda x: 'UNKNOWN' if type(x) != str else x)
all_data_df['HeatingDscr'] = all_data_df['HeatingDscr'].apply(lambda x: 'OTHER' if x == 'ELECTRIC WALL HEAT (1500W)' else x)
all_data_df['HeatingDscr'] = all_data_df['HeatingDscr'].apply(lambda x: 'OTHER' if x == 'GRAVITY' else x)
all_data_df['HeatingDscr'] = all_data_df['HeatingDscr'].apply(lambda x: 'OTHER' if x == 'RADIANT FLOOR' else x)
all_data_df['HeatingDscr'] = all_data_df['HeatingDscr'].apply(lambda x: 'OTHER' if x == 'WALL FURNACE' else x)
all_data_df['HeatingDscr'] = all_data_df['HeatingDscr'].apply(lambda x: 'OTHER' if x == 'AIR COND IN HEAT DUCTS' else x)
all_data_df['HeatingDscr'] = all_data_df['HeatingDscr'].apply(lambda x: 'OTHER' if x == 'HEAT PUMP' else x)
all_data_df['HeatingDscr'] = all_data_df['HeatingDscr'].apply(lambda x: 'OTHER' if x == 'SPACE HEATER' else x)
all_data_df['HeatingDscr'] = all_data_df['HeatingDscr'].apply(lambda x: 'OTHER' if x == 'BASEMENT HOT WATER' else x)
all_data_df['HeatingDscr'] = all_data_df['HeatingDscr'].apply(lambda x: 'OTHER' if x == 'nan' else x)
working_df = get_dummies(all_data_df, working_df, 'HeatingDscr')

all_data_df['Has_Asbestos'] = all_data_df['ExtWallDscrPrim'].apply(lambda x: 1 if x == 'FRAME ASBESTOS' else 0)
all_data_df['Has_Asbestos'] &= all_data_df['ExtWallDscrSec'].apply(lambda x: 1 if x == 'FRAME ASBESTOS' else 0)

print all_data_df['ExtWallDscrPrim'].describe()
get_dummies(all_data_df, working_df, 'ExtWallDscrPrim', join=False)
all_data_df['ExtWallDscrPrim'] = all_data_df['ExtWallDscrPrim'].apply(lambda x: 'OTHER' if type(x) != str else x)
all_data_df['ExtWallDscrPrim'] = all_data_df['ExtWallDscrPrim'].apply(lambda x: 'OTHER' if x == 'BLOCK STUCCO' else x)
all_data_df['ExtWallDscrPrim'] = all_data_df['ExtWallDscrPrim'].apply(lambda x: 'OTHER' if x == 'FAUX STONE' else x)
all_data_df['ExtWallDscrPrim'] = all_data_df['ExtWallDscrPrim'].apply(lambda x: 'OTHER' if x == 'FRAME ASBESTOS' else x)
all_data_df['ExtWallDscrPrim'] = all_data_df['ExtWallDscrPrim'].apply(lambda x: 'OTHER' if x == 'LOG' else x)
all_data_df['ExtWallDscrPrim'] = all_data_df['ExtWallDscrPrim'].apply(lambda x: 'OTHER' if x == 'METAL' else x)
all_data_df['ExtWallDscrPrim'] = all_data_df['ExtWallDscrPrim'].apply(lambda x: 'OTHER' if x == 'PAINTED BLOCK' else x)
all_data_df['ExtWallDscrPrim'] = all_data_df['ExtWallDscrPrim'].apply(lambda x: 'OTHER' if x == 'VINYL SIDING' else x)
all_data_df['ExtWallDscrPrim'] = all_data_df['ExtWallDscrPrim'].apply(lambda x: 'FRAME WOOD/SHAKE' if x == 'CEDAR SIDING' else x)  # only 2
working_df = get_dummies(all_data_df, working_df, 'ExtWallDscrPrim')

# exterior wall secondary
print all_data_df['ExtWallDscrSec'].describe()
get_dummies(all_data_df, working_df, 'ExtWallDscrSec', join=False)
all_data_df['ExtWallDscrSec'] = all_data_df['ExtWallDscrSec'].apply(lambda x: 'NONE' if type(x) != str else x)
all_data_df['ExtWallDscrSec'] = all_data_df['ExtWallDscrSec'].apply(lambda x: 'OTHER' if x == 'BLOCK STUCCO' else x)
all_data_df['ExtWallDscrSec'] = all_data_df['ExtWallDscrSec'].apply(lambda x: 'BRICK VENEER' if x == 'BRICK ON BLOCK' else x)
all_data_df['ExtWallDscrSec'] = all_data_df['ExtWallDscrSec'].apply(lambda x: 'OTHER' if x == 'CEDAR SIDING' else x)
all_data_df['ExtWallDscrSec'] = all_data_df['ExtWallDscrSec'].apply(lambda x: 'OTHER' if x == 'CEMENT BOARD SIDING' else x)
all_data_df['ExtWallDscrSec'] = all_data_df['ExtWallDscrSec'].apply(lambda x: 'OTHER' if x == 'FRAME ASBESTOS' else x)
all_data_df['ExtWallDscrSec'] = all_data_df['ExtWallDscrSec'].apply(lambda x: 'OTHER' if x == 'LOG' else x)
all_data_df['ExtWallDscrSec'] = all_data_df['ExtWallDscrSec'].apply(lambda x: 'OTHER' if x == 'METAL' else x)
all_data_df['ExtWallDscrSec'] = all_data_df['ExtWallDscrSec'].apply(lambda x: 'OTHER' if x == 'PAINTED BLOCK' else x)
all_data_df['ExtWallDscrSec'] = all_data_df['ExtWallDscrSec'].apply(lambda x: 'OTHER' if x == 'VINYL SIDING' else x)
working_df = get_dummies(all_data_df, working_df, 'ExtWallDscrSec')

print all_data_df['IntWallDscr'].describe()
get_dummies(all_data_df, working_df, 'IntWallDscr', join=False)
all_data_df['IntWallDscr'] = all_data_df['IntWallDscr'].apply(lambda x: 'UNKNOWN' if type(x) != str else x)
all_data_df['IntWallDscr'] = all_data_df['IntWallDscr'].apply(lambda x: 'OTHER' if x == 'PLYWOOD' else x)
all_data_df['IntWallDscr'] = all_data_df['IntWallDscr'].apply(lambda x: 'OTHER' if x == 'UNFINISHED' else x)
working_df = get_dummies(all_data_df, working_df, 'IntWallDscr')

print all_data_df['Roof_CoverDscr'].describe()
get_dummies(all_data_df, working_df, 'Roof_CoverDscr', join=False)
all_data_df['Roof_CoverDscr'] = all_data_df['Roof_CoverDscr'].apply(lambda x: 'UNKNOWN' if type(x) != str else x)
all_data_df['Roof_CoverDscr'] = all_data_df['Roof_CoverDscr'].apply(lambda x: 'UNKNOWN' if x == 'BUILT-UP' else x)
all_data_df['Roof_CoverDscr'] = all_data_df['Roof_CoverDscr'].apply(lambda x: 'UNKNOWN' if x == 'ROLL' else x)
all_data_df['Roof_CoverDscr'] = all_data_df['Roof_CoverDscr'].apply(lambda x: 'UNKNOWN' if x == 'TAR AND GRAVEL' else x)
working_df = get_dummies(all_data_df, working_df, 'Roof_CoverDscr')

print all_data_df['city'].describe()
get_dummies(all_data_df, working_df, 'city', join=False)
all_data_df['city'] = all_data_df['city'].apply(lambda x: 'UNINCORPORATED' if type(x) != str else x)
# all_data_df['city'] = all_data_df['city'].apply(lambda x: 'UNINCORPORATED' if x == 'BROOMFIELD' else x)
# eldorado springs, 585 pop above Boulder, so mountains
# https://www.google.com/maps/place/Eldorado+Springs,+CO/@39.9413104,-105.2961584,12.5z/data=!4m5!3m4!1s0x876b932fbfaf07c1:0xceb04ad53fcf5ce1!8m2!3d39.9324862!4d-105.2769348
all_data_df['city'] = all_data_df['city'].apply(lambda x: 'MOUNTAINS' if x == 'ELDORADO SPRINGS' else x)
# all_data_df['city'] = all_data_df['city'].apply(lambda x: 'UNINCORPORATED' if x == 'GOLDEN' else x)
all_data_df['city'] = all_data_df['city'].apply(lambda x: 'UNINCORPORATED' if x == 'HYGIENE' else x)
all_data_df['city'] = all_data_df['city'].apply(lambda x: 'MOUNTAINS' if x == 'JAMESTOWN' else x)
all_data_df['city'] = all_data_df['city'].apply(lambda x: 'MOUNTAINS' if x == 'WARD' else x)
working_df = get_dummies(all_data_df, working_df, 'city')

# http://stackoverflow.com/questions/29530232/python-pandas-check-if-any-value-is-nan-in-dataframe
if not working_df.isnull().values.any():
    print 'No null values'
else:
    print 'Null Values Found!!!'

    for col in working_df:
        if working_df[col].isnull().values.any():
            print '%s has null values' % col

print 'Shape, working df: %s' % str(working_df.shape)
print 'Length, Working DF %s' % len(working_df.index)

working_df.reset_index(drop=True, inplace=True)
working_df.to_csv('Data\\$working_data_5jnk.csv', index=False)
print 'Done, file saved'
