#!/bin/bash
INFILE=./key.txt
export FINN="$(cat "$INFILE")"
rm ./key.txt

python server.py &
sleep 2
streamlit run app.py
