# Streamlit Websocket Application

In the Dockerfile there is an ENV created for "BCSV", which is the location where the "data.csv" file is being written when the application is run. It's currently set to WORKDIR, as the csv is written to the same relative location locally.

The Dockerfile also moves a "key.txt" file into its container image. This file contains the Finnhub API key. You'll need to create this file with your own API key in order to run this app at all.

Deploying to Heroku via CLI:
heroku login
heroku container:login
heroku container:push web -a <image_name>
heroku container:release web -a <image_name>
heroku open -a <image_name>