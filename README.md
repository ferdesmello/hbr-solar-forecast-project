# hbr-solar-forecast-project

## Overview
I developed this project as the final activity of the first phase of the course Residência em Tecnologias Aeroespaciais - Inteligência Artificial offered by Instituto Hardware BR, applying what I learning in the course to solve an aerospace problem.

I choose [space weather](https://en.wikipedia.org/wiki/Space_weather) forecasting, especially the forecasting of [solar flares](https://en.wikipedia.org/wiki/Solar_flare) and [geomagnetic storms](https), as space weather can significantly impact communications, the electrical grid, satellites, and astronauts in orbit.

Please, read [the project documentation](https://github.com/ferdesmello/hbr-solar-forecast-project/tree/main/Fernando%20Mello%20-%20previsão%20de%20flares%20e%20tempestades%20geomagnéticas.pdf) (in Portuguese) or watch this [short video presentation](https://youtu.be/IQgli0LVTLw) (in Portuguese) for more details.

![Pictures of the main events.](./figures/Sun's%20things.jpg "Solar and terrestrial events related to space weather. a) A large cluster of sunspots. Credit: NASA/SDO/AIA. b) A large solar flare seen in X-rays. Credit: NASA/SDO. c) A large coronal mass ejection with a coronagraph obscuring the view of the Sun. Credit: NASA/GSFC/SOHO. d) Aurora australis seen from the International Space Station. Credit: NASA.")
Figure: Solar and terrestrial events related to space weather. a) A large cluster of sunspots. Credit: NASA/SDO/AIA. b) A large solar flare seen in X-rays. Credit: NASA/SDO. c) A large coronal mass ejection with a coronagraph obscuring the view of the Sun. Credit: NASA/GSFC/SOHO. d) Aurora australis seen from the International Space Station. Credit: NASA.

## Repository structure

<pre>
├── data/                           # Where all the datasets are stored
├── downloaders/                    # Scripts to download the raw datasets
│   ├── downloader_Dst.py
│   ├── downloader_GOES_xray.py
│   ├── downloader_OMNI.py
│   └── downloader_SHARP.py
├── figures/                        # Final figures with forecasts' results
├── filters/                        # Scripts to clean and reduce the raw datasets
│   ├── filter_flares.ipynb
│   └── filter_storms.ipynb
├── forecasters/                    # Scripts to make the forecasts
│   ├── forecast_flares_NN.ipynb
│   ├── forecast_flares_RF.ipynb
│   ├── forecast_flares_RNN.ipynb
│   ├── forecast_flares_SVM.ipynb
│   ├── forecast_storms_NN.ipynb
│   ├── forecast_storms_RF.ipynb
│   ├── forecast_storms_RNN.ipynb
│   └── forecast_storms_SVM.ipynb
├── LICENSE
└── README.md                       # This document
</pre>

## What the code does

### 1. Downloading the data

I wrote scripts to access and download data from two main sources:

* [PySPEDAS](https://pyspedas.readthedocs.io/en/latest/index.html), a Python library that offers many types of data from the Sun. I used it for:
  * [GOES](https://pyspedas.readthedocs.io/en/latest/goes.html), to access data of the [GOES](https://www.ospo.noaa.gov/operations/goes/) satellite missions.
  * [OMNI](https://pyspedas.readthedocs.io/en/latest/geomagnetic_indices.html#omni-solar-wind-and-magnetospheric-indices), to access data from many different instruments and missions. I used it for a mix of data.
* [DRMS](https://docs.sunpy.org/projects/drms/en/stable/), a Python library to access a variety of spaceweather quantities. I used it for [SHARP](http://jsoc.stanford.edu/doc/data/hmi/sharp/sharp.htm) data.

And I used a dataset available at Kaggle:

* [Solar + Geomagnetic Indices: EDA](https://www.kaggle.com/code/erevear/solar-geomagnetic-indices-eda/input?select=daily_solar_data.csv).

The scripts are in the [downloaders](https://github.com/ferdesmello/hbr-solar-forecast-project/tree/main/downloaders) folder.

The downloaded files are saved in the [data](https://github.com/ferdesmello/hbr-solar-forecast-project/tree/main/data) folder, but are too large to include in this repository.

#

### 2. Cleaning the data

The datasets have many null values, windows of no data, or the data were taken at different time paces. I cleaned and merged the datasets into two: one for the solar flares (data_flares.csv) and one for the geomagnetic storms (data_storms.csv), which you can find in the [data](https://github.com/ferdesmello/hbr-solar-forecast-project/tree/main/data) folder.

The cleaning scripts are in the [filters](https://github.com/ferdesmello/hbr-solar-forecast-project/tree/main/filters) folder.

#

### 3. The models

The goal is to predict the presence or absence of flares or storms in the next day (flare) or hour (storm) based on the last three days (flare) or hours (storms). I used each dataset to train 4 types of models:

* Random Forest (RF).
* Support Vector Machine (SVM).
* Neural Network (NN).
* Recurrent Neural Network - Gated Recurrent Unit (RNN-GRU).

The first two I built using [scikit-learn](https://scikit-learn.org/stable/), and the last two, using [tensorflow-keras](https://www.tensorflow.org/guide/keras).
I had to shape the datasets a bit to fit the use in each model, but it was a small change, mostly separating features from target, standardizing features using a scaler, and creating new lagged features.

The models are in the [forecasters](https://github.com/ferdesmello/hbr-solar-forecast-project/tree/main/filters) folder.

#

### 4. The figures

For each model, I made a set of figures showing metrics and results.

The figures are in the [figures](https://github.com/ferdesmello/hbr-solar-forecast-project/tree/main/filters) folder.

An example of a resulting figure for the geomagnetic storm RNN-GRU model:

![A final plot as an example.](./figures/geomag_storm_RNN_results.png "Results of the RNN-GRU model for geomagnetic storms.")
