#!/bin/bash
#add authentication information
export GOOGLE_APPLICATION_CREDENTIALS="authentication/tutor-qnddyp-7df36744e00c.json"
#run web server end
python3 src/service.py
