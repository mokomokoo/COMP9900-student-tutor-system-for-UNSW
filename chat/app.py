# import flask dependencies
from flask import Flask, request, make_response, jsonify
import os
from crawler import *
import manager

# initialize the flask app
app = Flask(__name__)

#used to call web spider to get corresponding information
def crawler(CourseId, intents):
    message = get_data(CourseId)[intents]
    return message

#check whether this course offered or not inthis term
def check_t(CourseId):
    timetable = get_timetable(CourseId)
    if timetable:
        return True
    else:
        return False


# function for dialog management to output responses based on 
# deal with different reponse based on intents
def course_info():

    # build a request object
    # get related important factors from query result
    req = request.get_json(force=True)
    query_result = req.get('queryResult')
    # debug use 
    # print(query_result)
    action = query_result.get('action')
    params = query_result.get('parameters')
    intents = query_result.get('intent').get('displayName')

    #
    if intents != 'askKB':
        CourseId = params.get('CourseId')
        # CourseId = re.sub(r'([a-zA-Z]{4}) - ([0-9]) - ([0-9]{3})', r'\1\2\3', CourseId)

    #different intents get different feedback
    if intents == "courseInfo":
        info = get_data(CourseId)
        message = "\n".join(i+': '+str(info[i]) for i in info.keys())
        # denug use 
        # print("message:", message)

    elif intents == 'courseInfo - custom':
        message = 'For more information about this course, click handbook link: ' + crawler(CourseId, 'handbook Link')

    elif intents == "Overview":
        message = crawler(CourseId, intents)

    elif intents == 'Timetable':
        if check_t(CourseId):
            message = 'You can click this link to see timetable: ' + crawler(CourseId, 'timetable Link')
        else:
            message = 'This course is not offered in this term!'

    elif intents == "Lecturer":
        if check_t(CourseId):
                message = "The Lecturer of this course is: " + crawler(CourseId, intents)
        else:
            message = 'This course is not offered in this term!'

    elif intents == 'Census':
        if check_t(CourseId):
                message = 'The Census Date is: '+ crawler(CourseId, 'timetable')['Census Date']+", which is the last day of dropping this course."
        else:
            message = 'This course is not offered in this term!'

    elif intents == 'Enrols':
        if check_t(CourseId):
                message = crawler(CourseId, intents)
        else:
            message = 'This course is not offered in this term!'

    elif intents == 'Status':
        if check_t(CourseId):
            message = "The status of this course is: " + crawler(CourseId, intents)
        else:
            message = 'This course is not offered in this term!'

    elif intents == 'Faculty':
        faculty = crawler(CourseId, intents)
        school = crawler(CourseId, 'School')
        message = "Faculty: " + faculty + ", School: " + school

    elif intents == 'OfferTerms':
        message = "This course is offered in " + crawler(CourseId, 'Offering Terms')

    elif intents == 'Prerequisite':
        prerequisite = crawler(CourseId, intents)
        if prerequisite:
            message = 'The Prerequisite of this course are: ' + prerequisite
        else:
            message = 'There is no prerequisite for this course.'

    elif intents == 'Study Level':
        message = "The Study Level of this course is: "+ crawler(CourseId, intents)

    elif intents == 'Unit of Credit':
        message = "Unit of Credit for this course is: " + crawler(CourseId, intents)

    elif intents == 'askKB':
        message = manager.find(params['Concept'])

    return {'fulfillmentText': message}    



# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(course_info()))

# run the app
if __name__ == '__main__':
    port = int(os.getenv("PORT", 5001))
    print("start port on %d" %(port))
    app.run(debug=True, port=port, host='0.0.0.0')