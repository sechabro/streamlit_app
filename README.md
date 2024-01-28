# streamlit_app

In the Dockerfile there is an ENV created for "BCSV", which is the location where the "data.csv" file is being written when the application is run. It's currently set to WORKDIR, as the csv is written to the same relative location locally.

The Dockerfile also moves a "key.txt" file into its container image. This file contains the Finnhub API key. You'll need to create this file with your own API key in order to run this app at all.

Within "docker_run.sh", the API key is read and set as an environment variable "FINN", the value for which is retrieved by "server.py" upon application startup.