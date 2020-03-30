import requests
import numpy as np
import csv
from datetime import datetime, date, timedelta
import urllib.request
import pandas as pd
import os

def get_data(days_back=1):
    summary_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{}.csv'.format(
        datetime.today().strftime('%m-%d-%Y'))
    try:
        urllib.request.urlopen(summary_url)
    except:
        #if no update exists for today, go to yesterday...if that fails, plug in days back until you get data
        yesterday = date.today() - timedelta(days=days_back)
        summary_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{}.csv'.format(
            yesterday.strftime('%m-%d-%Y'))
    with requests.Session() as s:
        download = s.get(summary_url)
        decoded_content = download.content.decode('utf-8')
        reader = csv.DictReader(decoded_content.splitlines(), delimiter=',')
        return reader


def get_country_metric(metric_type,country):
    metric_arr = np.array([row[metric_type] for row in summary if row['Country_Region'] == country]).astype(np.float)
    metric = np.sum(metric_arr)
    return metric

summary = get_data()

us_confirmed = get_country_metric('Confirmed','US')
us_deaths = get_country_metric('Deaths','US')
us_recovered = get_country_metric('Recovered','US')
us_active = get_country_metric('Active','US')
china_confirmed = get_country_metric('Confirmed','China')
china_deaths = get_country_metric('Deaths','China')
china_recovered = get_country_metric('Recovered','China')
china_active = get_country_metric('Active','China')

#TS data - these are expected to be deprecated soon and switched to new format

try:
    global_confirmed_ts = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
except:
    print('Confirmed time series data has moved, check URL')
try:
    global_deaths_ts = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
except:
    print('Deaths time series data has moved, check URL')
try:
    global_recovered_ts = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
except:
    print('Recovered time series data has moved, check URL')

asia_summary = pd.read_csv(os.getcwd()+'/Data/asia_health_summary.csv')
asia_hospital = pd.read_csv(os.getcwd()+'/Data/asia_hospital_data.csv')
us_hospital = pd.read_csv(os.getcwd()+'/Data/us_hospital_summary.csv')

# save dataframes for confirmed, deaths, and recovered for just US and china
china_confirmed_ts = pd.DataFrame(global_confirmed_ts[global_confirmed_ts['Country/Region'] == 'China'].loc[:,'1/22/20':].sum())
china_deaths_ts = pd.DataFrame(global_deaths_ts[global_deaths_ts['Country/Region'] == 'China'].loc[:,'1/22/20':].sum())
china_recovered_ts = pd.DataFrame(global_recovered_ts[global_recovered_ts['Country/Region'] == 'China'].loc[:,'1/22/20':].sum())
us_confirmed_ts = global_confirmed_ts[global_confirmed_ts['Country/Region'] == 'US'].loc[:,'1/22/20':].T
us_deaths_ts = global_deaths_ts[global_deaths_ts['Country/Region'] == 'US'].loc[:,'1/22/20':].T
us_recovered_ts = global_recovered_ts[global_recovered_ts['Country/Region'] == 'US'].loc[:,'1/22/20':].T

# convert indices to datetime objects
china_deaths_ts.index = pd.to_datetime(china_deaths_ts.index)
china_recovered_ts.index = pd.to_datetime(china_recovered_ts.index)
china_confirmed_ts.index = pd.to_datetime(china_confirmed_ts.index)
us_deaths_ts.index = pd.to_datetime(us_deaths_ts.index)
us_recovered_ts.index = pd.to_datetime(us_recovered_ts.index)
us_confirmed_ts.index = pd.to_datetime(us_confirmed_ts.index)

us_deaths_ts.columns = ['deaths']
china_deaths_ts.columns = ['deaths']
us_confirmed_ts.columns = ['confirmed']
china_confirmed_ts.columns = ['confirmed']

# get stats for us and china
china = asia_hospital[asia_hospital['Country and Region '] == 'China ']
# taking care of data entry issues
icu_china = pd.to_numeric(china['ICU Beds '].str.replace(',', ''))
# get us icu info
icu_cols = [col for col in us_hospital.columns if 'intensive' in col.lower()]
icu_us = sum([pd.to_numeric(us_hospital[col].str.replace(',', '')) for col in icu_cols])
# population information
pop_us = 329_444_452 #source: https://www.census.gov/popclock/
pop_china = 1_401_972_080  #source: http://data.stats.gov.cn/english/

# convert to df to plot in Tableau
stats = [{'location': 'China',
          'icu_beds': icu_china.iloc[0],
          'pop': pop_china,
          'beds_per_100000': icu_china.iloc[0]/(pop_china/100_000)},
         {'location': 'United States',
          'icu_beds': icu_us.iloc[0],
          'pop': pop_us,
          'beds_per_100000': icu_us.iloc[0]/(pop_us/100_000)}]
icu_beds_df = pd.DataFrame(stats, columns=['location', 'icu_beds', 'pop', 'beds_per_100000'], index=['China', 'US'])
icu_beds_df.to_csv('./Data/icu_beds.csv')

stats = pd.read_csv('./Data/icu_beds.csv', index_col='location')
# china took 88 days to reach icu capacity for # of confirmed cases
# first china confirmed case nov 17
# https://www.theguardian.com/world/2020/mar/13/first-covid-19-case-happened-in-november-china-government-records-show-report
print(china_confirmed_ts[china_confirmed_ts['confirmed'] >= stats.loc['China','icu_beds']])
print(pd.to_datetime('2020-02-13') - pd.to_datetime('2019-11-17'))
# us took 66 days to reach icu capacity for # of confirmed cases
print(us_confirmed_ts[us_confirmed_ts['confirmed'] >= stats.loc['United States','icu_beds']].head(1))
print(pd.to_datetime('2020-03-28') - pd.to_datetime('2020-01-22'))

#save for visualizations
us_confirmed_ts.to_csv('./Data/us_confirmed_ts.csv')
china_confirmed_ts.to_csv('./Data/china_confirmed_ts.csv')
