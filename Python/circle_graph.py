import requests
import numpy as np
import csv
from datetime import datetime, date, timedelta
import urllib.request

def get_data():
    summary_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{}.csv'.format(
        datetime.today().strftime('%m-%d-%Y'))
    try:
        urllib.request.urlopen(summary_url)
    except:
        yesterday = date.today() - timedelta(days=1)
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
