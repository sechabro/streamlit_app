#!/bin/bash
INFILE=./key.txt
DIR=./
export FINN="$(cat "$INFILE")"

python server.py &
sleep 10
streamlit run app.py
