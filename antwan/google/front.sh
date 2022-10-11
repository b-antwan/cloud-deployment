#!/bin/bash
cd /home/antoine_blancy
sed -i '1c\const backaddr = "http://34.65.100.167";' script.js
python3 -m http.server