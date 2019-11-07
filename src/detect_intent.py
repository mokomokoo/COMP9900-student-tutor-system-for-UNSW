#!/usr/bin/env python3

import dialogflow
import os

from google.api_core.exceptions import InvalidArgument
#add authentication information for dialogflow
DIALOGFLOW_PROJECT_ID = 'tutor-qnddyp'
DIALOGFLOW_LANGUAGE_CODE = 'en-US'
GOOGLE_APPLICATION_CREDENTIALS = "./tutor-qnddyp-7df36744e00c.json"
# SESSION_ID = '1' #current user id

#detect intents of 5the user based on their input
def detect_intents(input_text, SESSION_ID='1'):

    #create session
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    #input text
    text = dialogflow.types.TextInput(text=input_text, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query = dialogflow.types.QueryInput(text=text)
    #get response
    try:
        response = session_client.detect_intent(session=session, query_input=query)
    except InvalidArgument:
        raise

    # for debug use
    # print("query:", response.query_result.query_text)
    # print("detected intent", response.query_result.intent.display_name)
    # print("confidence", response.query_result.intent_detection_confidence)
    return response.query_result
