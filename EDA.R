# Exploratory Data Analysis in R
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

rm(list = ls())
library(ggplot2)
# http://www.cookbook-r.com/Graphs/Colors_(ggplot2)/
cbPalette <- c("#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")

# set up the data
setwd("C:\\Users\\Kevin\\PycharmProjects\\MSDS692\\Data")

df <- read.csv('$working_data_5c.csv', header = TRUE)
df <- df[df$totalActualVal <= 2000000, ]
df <- df[df$Age_Yrs > 0, ]

table(df$designCodeDscr)
table(df$city)
table(df$Roof_CoverDscr)
table(df$IntWallDscr)
table(df$ExtWallDscrPrim)
table(df$ExtWallDscrSec)
table(df$HeatingDscr)
table(df$AcDscr)
table(df$carStorageType)
table(df$carStorageTypeDscr)
table(df$deed_type)
table(df$nbrRoomsNobath)

summary(df$TotalFinishedSF)
df_sf0 <- df[df$TotalFinishedSF < 100, ]
df <- df[df$TotalFinishedSF > 1 & df$TotalFinishedSF < 15000, ]

plot(df$totalActualVal, df$price)
plot(df$TotalFinishedSF, df$price)
plot(df$GIS_sqft, df$price)

df$nbrFullBaths
df$nbrHalfBaths
df$nbrThreeQtrBaths
df$TotalBaths <- df$nbrFullBaths + df$nbrHalfBaths + df$nbrThreeQtrBaths
df$deed_type
df$carStorageType
df$designCodeDscr
df$AcDscr


ggplot(df, aes(x=totalActualVal, y=price)) + geom_point(shape=1, color=cbPalette[3])
ggplot(df, aes(x=TotalFinishedSF, y=price)) + geom_point(shape=1, color=cbPalette[3])
ggplot(df, aes(x=GIS_sqft, y=price)) + geom_point(shape=1, color=cbPalette[3])
ggplot(df, aes(x=nbrRoomsNobath, y=price)) + geom_point(shape=1, color=cbPalette[3])
ggplot(df, aes(x=TotalBaths, y=price)) + geom_point(shape=1, color=cbPalette[3])
ggplot(df, aes(x=Age_Yrs, y=price)) + geom_point(shape=1, color=cbPalette[3])

ggplot(df, aes(deed_type, price)) + geom_boxplot()
ggplot(df, aes(carStorageType, price)) + geom_boxplot()
ggplot(df, aes(designCodeDscr, price)) + geom_boxplot()
ggplot(df, aes(AcDscr, price)) + geom_boxplot()
# https://stackoverflow.com/questions/1330989/rotating-and-spacing-axis-labels-in-ggplot2
ggplot(df, aes(ExtWallDscrPrim, price)) + geom_boxplot() + theme(axis.text.x=element_text(angle=45, hjust=1))
ggplot(df, aes(ExtWallDscrSec, price)) + geom_boxplot() + theme(axis.text.x=element_text(angle=45, hjust=1))

# boxplot for nbr of rooms no bath
df$nbrRoomsNobath[df$nbrRoomsNobath == 0] <- 1
df$nbrRoomsNobath[df$nbrRoomsNobath > 15] <- 15
ggplot(df, aes(as.factor(nbrRoomsNobath), price)) + geom_boxplot()

# scatter plot for age in years
ggplot(df, aes(x=Age_Yrs, y=price)) + geom_point(shape=1, color=cbPalette[3])
ggplot(df, aes(x=Time_Period, y=price)) + geom_point(shape=1, color=cbPalette[3])

df.age <- df[df$Age_Yrs < 30, ]
ggplot(df.age, aes(as.factor(Age_Yrs), TotalFinishedSF)) + geom_boxplot()

