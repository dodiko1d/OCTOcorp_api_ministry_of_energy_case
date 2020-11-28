import os
import logging
from math import sqrt
from subprocess import call
from datetime import datetime, timedelta
import csv
import requests
import numpy as np
import pandas as pd
import statsmodels.api as sm
from bs4 import BeautifulSoup
from statsmodels.tsa.arima_model import ARIMAResults


def get_load_data(date):
    url = "http://www.delhisldc.org/Loaddata.aspx?mode="
    logger.info("Scraping " + date)
    resp = requests.get(url + date)
    soup = BeautifulSoup(resp.text, "lxml")
    table = soup.find(
        "table", {"id": "ContentPlaceHolder3_DGGridAv"}
    )
    trs = table.findAll("tr")
    if len(trs[1:]) == 288:
        with open(
            "monthdata.csv", "a"
        ) as f:
            writer = csv.writer(f)
            for tr in trs[1:]:
                time, delhi = tr.findChildren("font")[:2]
                writer.writerow([date + " " + time.text, delhi.text])
    if len(trs[1:]) != 288:
        logger.info("Some of the load values are missing..")
    else:
        logger.info("Done")


def get_data():
    return pd.read_csv(
        "monthdata.csv",
        header=None,
        index_col=["datetime"],
        names=["datetime", "load"],
        parse_dates=["datetime"],
        infer_datetime_format=True,
    )


logging.basicConfig(
    filename="aws_arima_log.txt",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)
logger = logging.getLogger()
console = logging.StreamHandler()
logger.addHandler(console)

if os.path.exists("monthdata.csv"):
    data = get_data()
    if (datetime.today() - timedelta(1)).date().strftime('%Y-%m-%d') == str(data.index.date[-1]):
        yesterday = datetime.today() - timedelta(1)
        yesterday = yesterday.strftime("%d/%m/%Y")
        get_load_data(yesterday)
        data = get_data()
        day_to_clip_from = datetime.today() - timedelta(30)
        logger.info("Clipping data from " + day_to_clip_from.strftime("%d/%m/%Y"))
        data = data[day_to_clip_from.strftime("%d/%m/%Y"):]
        data.to_csv(
            "monthdata.csv", header=False
        )
    else:
        logger.info('Yesterday"s load already parsed!')
else:
    for i in range(31, 0, -1):
        yesterday = datetime.today() - timedelta(i)
        yesterday = yesterday.strftime("%d/%m/%Y")
        get_load_data(yesterday)
    data = get_data()



logger.info(data.shape)
data = data.asfreq(freq="30Min", method="bfill")

# initialize the model
model = sm.tsa.statespace.SARIMAX(
    data,
    order=(3, 1, 1),
    seasonal_order=(3, 0, 0, 24),
    enforce_stationarity=False,
    enforce_invertibility=False,
)

# fit the model with the data
logger.info("Starting model fitting...")
model = model.fit()

logger.info("Model fitting done!!")
logger.info(model.summary().tables[1])
logger.info(model.summary())

# save the model
model.save("ARIMA_month_model.pkl")

todays_date = datetime.today().strftime("%d/%m/%Y")
tommorows_date = (datetime.today() + timedelta(1)).strftime("%d/%m/%Y")

pred = model.get_prediction(
    start=data.shape[0],
    end=data.shape[0]+48,
    dynamic=False,
)

predictions = pred.predicted_mean
predictions = predictions.asfreq(freq="5Min", method="bfill")
date = datetime.today().strftime(format="%d-%m-%Y")
predictions.to_csv(
    "predictions/ARIMA/%s.csv" % date, index_label="datetime", header=["load"]
)

error = sqrt(((predictions - np.squeeze(todays_date['%s' % date:]))**2).mean())
logger.log(error)


