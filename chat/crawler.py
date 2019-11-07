import requests
import re
from bs4 import BeautifulSoup
# crawl the information in timetable
def get_timetable(course_id, teaching_period='T2'):
    timetable = {}
    url_timetable = "http://timetable.unsw.edu.au/2019/"+course_id.upper()+".html" 
    timetable["timetable Link"] = url_timetable
    r = requests.get(url_timetable)
    soup = BeautifulSoup(r.text, 'lxml')
    data = soup.select('td .data')
    f = 0
    n = 0
    for item in data:
        if item.getText() == teaching_period:
            f += 1
            n += 1
            continue
        if f == 1:
            lecturer = item.getText()
            f = 2
            timetable["Lecturer"] = lecturer
#            print("Lecturer:",lecturer)
            continue
        if f == 2:
            census_date = item.getText()
            f += 1
            timetable["Census Date"] = census_date
#            print("Census_Date:",Census_Date)
            continue
        if item.font:              
            status = item.font.getText()
            if (status == "Open" or status == "Full") and n == 2:
                f = 5
                timetable["Status"] = status
#                print("Status:",status)
            continue
        if f == 5:
            enrols = item.getText()
            f += 1
            timetable["Enrols"] = enrols
#            print("Enrols:",Enrols)
            break
    if n == 0:
        timetable = {}
#        print(course_id,"is not availible in",Teaching_Period)
#    print("Click",url_timetable,"for more details.")
    return timetable

# crawl the information in handbook
def get_handbook(course_id):
    handbook = {}
    url_handbook = "https://www.handbook.unsw.edu.au/postgraduate/courses/2019/"+course_id
    r = requests.get(url_handbook)
    soup = BeautifulSoup(r.text, 'lxml')
    overview = soup.select('div .a-card-text')[0].getText().split("\n")[2]
    handbook["Overview"] = overview
#    print("Overview:",Overview)
    unit_of_credit = soup.select('div h4 strong')[1].getText()
    handbook["Unit of Credit"] = unit_of_credit
#    print("Unit of Credit:",Unit_of_credit)
    prerequisite = soup.select('div .a-card-text')
    if len(prerequisite) > 1:
        prerequisite = prerequisite[1].getText().strip().split(" ")[1]
    else:
        prerequisite = None
    handbook["Prerequisite"] = prerequisite
#    print("Prerequisite:",Prerequisite)
    study_level = soup.select('.enable-helptext')[1].getText()
    handbook["Study Level"] = study_level
#    print("Study Level:",Study_level)
    faculty_school = soup.find_all('a',attrs={"target":"_blank"})
    
    for item in faculty_school:
        item = item.getText()
        if re.match("^Faculty", item):
            faculty = item
            continue
        if re.match("^School", item):
            school = item
            continue
    handbook["Faculty"] = faculty
    handbook["School"] = school
#    print("Faculty:",f)
#    print("School:",s)
    offering_terms = soup.find_all('p',attrs={"tabindex":"0","class":""})[0].getText()
    handbook["Offering Terms"] = offering_terms
#    print("Offering Terms:",Offering_terms)
    handbook["handbook Link"] = url_handbook
#    print("Click",url_handbook,"for more details.")
    return handbook

def get_data(course_id, teaching_period='T2'):
    handbook_result = get_handbook(course_id)
    timetable_result = get_timetable(course_id, teaching_period)
    for item in timetable_result:        
        handbook_result[item] = timetable_result[item]
    return handbook_result
    
#if __name__ == '__main__':
#    course_id = 'comp9318'
#    teaching_period = 'T1'
#    a = get_data(course_id, teaching_period)
#    for i in a:
#        print(i,":\n",a[i])
#    print("\n\n",a)

    
    