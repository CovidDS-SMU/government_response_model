from covid.api import CovId19Data
import numpy as np
from sklearn.linear_model import LinearRegression as lr
import os
import csv

#collect data
api = CovId19Data(force=False)
res = api.get_all_records_by_country()
with open(os.getcwd()+'/Data/democracy_index_2019_table.csv', mode='r') as f:
    reader = csv.reader(f)
    next(reader)
    govt = {rows[0]:rows[1:] for rows in reader}

#basic regression against rates, since not all countries report their rates we will need to match first
#reports = [res[x]['label'] for x in res.keys()]
dem_idx = np.array([govt[x][0] for x in govt.keys()]).astype(np.float).reshape(-1,1)
conf = np.array([res[x]['confirmed'] for x in res.keys()])
#conf = np.pad(conf, 1, mode='mean')
death = np.array([res[x]['deaths'] for x in res.keys()])
recv = np.array([res[x]['recovered'] for x in res.keys()])

#reg_conf = lr().fit(dem_idx, conf)
#reg_conf.score(dem_idx, conf)
print(conf)
print(dem_idx)