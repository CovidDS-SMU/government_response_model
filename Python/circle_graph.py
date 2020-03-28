import requests
import numpy as np
import csv
from datetime import datetime, date, timedelta
import urllib.request
import pandas as pd

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
