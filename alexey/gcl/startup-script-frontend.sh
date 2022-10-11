#!/bin/bash
cd /home/alexe/frontend/
sed -i '1s/.*/const backaddr = "34.122.140.81";/' script.js
http-server -p 8000
