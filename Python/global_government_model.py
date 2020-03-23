from covid.api import CovId19Data
import numpy as np
from sklearn.linear_model import LinearRegression as lr
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import os
import csv

#collect data
api = CovId19Data(force=False)
res = api.get_all_records_by_country()
with open(os.getcwd()+'\Data\democracy_index_2019_table.csv', mode='r') as f:
    reader = csv.reader(f)
    next(reader)
    govt = {rows[0]:rows[1:] for rows in reader}

#basic regression against rates, since not all countries report their rates we will need to match first
#reports = [res[x]['label'] for x in res.keys()]
dem_idx = np.array([govt[x][0] for x in govt.keys()]).astype(np.float).reshape(-1,1)
conf = np.array([res[x]['confirmed'] for x in res.keys()])
conf = np.append(conf, np.median(conf))
death = np.array([res[x]['deaths'] for x in res.keys()])
recv = np.array([res[x]['recovered'] for x in res.keys()])

reg_conf = lr().fit(dem_idx, conf)
print(reg_conf.score(dem_idx, conf))

# Split the data into training/testing sets
#dem_train = dem_idx[:-20]
#dem_test = dem_idx[-20:]

# Split the targets into training/testing sets
#conf_train = conf[:-20]
#conf_test = conf[-20:].reshape(-1,1)

# Train the model using the training sets
#conf_lr = lr().fit(dem_train, conf_train)

# Make predictions using the testing set
#conf_pred = conf_lr.predict(conf_test)

# The coefficients
#print('Coefficients: \n', conf_lr.coef_)
# The mean squared error
#print('Mean squared error: %.2f'
#      % mean_squared_error(conf_test, conf_pred))
# The coefficient of determination: 1 is perfect prediction
#print('Coefficient of determination: %.2f'
#      % r2_score(conf_test, conf_pred))

# Plot outputs
#plt.scatter(dem_test, conf_test,  color='black')
plt.plot(dem_idx, color='blue', linewidth=3)
plt.plot(conf, color='yellow', linewidth=3)
plt.xticks(())
plt.yticks(())

plt.show()