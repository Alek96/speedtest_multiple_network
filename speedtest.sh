#/bin/bash

test="speedtest --json --server 7103"
outputFile="$(dirname "$0")/tests.json"

echo "$($test)" >> "$outputFile"

