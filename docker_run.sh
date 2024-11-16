#!/bin/bash
INFILE=./key.txt
export FINN="$(cat "$INFILE")"
rm ./key.txt