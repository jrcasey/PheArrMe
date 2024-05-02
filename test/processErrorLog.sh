#!bin/bash

cat error.log | grep "Command failed" | sed 's/Command failed for medium //' | sed 's/://' > problemMedia
