#!/bin/bash
INFILE=./key.txt
DIR=./
export FINN="$(cat "$INFILE")"

python server.py &
sleep 5
streamlit run app.py
