#!/bin/bash
cd /home/antoine_blancy/
sed -i '1c\const backddr = "130.211.201.255";' script.js
python3 -m http.server