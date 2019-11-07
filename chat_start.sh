#!/bin/bash

#expose local service to the internet
ssh -R chatbot:80:localhost:5001 serveo.net >/dev/null 2>&1 &

#run app to connect with dialogflow webbhook
python3 chat/app.py 
