from course import Course
import json
from json import JSONEncoder
from enum import Enum
from colorama import Back, init
import re

#ensures colored prints using "colorama" package will reset automatically afterwards
init(autoreset=True)

"""
classes
"""
#class MENU_ACTIONS - Enum inherited class for menu actions
class MENU_ACTIONS(Enum):
    DISPLAY_STUDENT = 1
    REGISTER_COURSE = 2
    REMOVE_COURSE = 3
    DISPLAY_TIMETABLE = 4
    DISPLAY_EXAMS = 5
    LOGOFF = 6

#class SEARCH_TYPES - Enum inherited class for types of search
class SEARCH_TYPES(Enum):
    SEARCH_BY_NAME = 1
    SEARCH_BY_NUM = 2
    SEARCH_BY_POINTS = 3
    SEARCH_BY_DAYS = 4
    SEARCH_ALL_COURSES = 5
#class CourseEncoder - encodes course object to json format
class CourseEncoder(JSONEncoder):
    def default(self, obj):
        return {"name": obj.name, "num": obj.num, "points": obj.points, "timeLectures": obj.timeLectures, "timeTutorial": obj.timeTutorial, "exams": obj.exams, "maxstud": obj.maxstud, "enlistedstud": obj.enlistedstud}
#class CourseEncoder - encodes student object to json format
class StudentEncoder(JSONEncoder):
    def default(self, obj):
        #transforming all course objects for each student to dictionaries using builddicts
        coursearr = StudentEncoder.builddicts(obj.courselst)
        return {"name": obj.name, "ID": obj.ID, "courselst": coursearr}
    #FUNCTION: builddicts - makes a dictionary for an obejct in a list if the object is not already a dictionary. returns a list of dictionaries
    def builddicts(objlst):
        res = []
        for item in objlst:
            if type(item) != dict:
                res.append(item.__dict__)
            else:
                res.append(item)
        return res
    
"""
functions
"""
#FUNCTION: course_decoder - decodes course object from a dictionary
def course_decoder(jsondict):
    course = Course(name=jsondict["name"], num=jsondict["num"], points=jsondict["points"], timeLectures=jsondict["timeLectures"], timeTutorial=jsondict["timeTutorial"], exams=jsondict["exams"], maxstud=jsondict["maxstud"], enlistedstud=jsondict["enlistedstud"])
    return course
  
#FUNCTION: find_courses_by_num - recieves a list of dictionary variants of courses and returns a list of all courses objects in correlation to the input 
def find_courses_by_num(coursesdict):
    res = []
    for item in coursesdict:
        for course in Course.allcourses:
            #checks if course number is the value of key "num" of present item (item is a course dictionary)
            if course.num == item["num"]:
                res.append(course)
    return res
#FUNCTION: student_decoder - decodes student object from a dictionary
def student_decoder(jsondict):
    from student import Student
    if(jsondict.get("num")):
        return jsondict
    #student object contains an attribute of course objects, therefore create a list of course objects using find_courses_by_num
    courses = find_courses_by_num(jsondict["courselst"])
    student = Student(name=jsondict["name"], ID=jsondict["ID"], courselst= courses)
    return student    

#FUNCTION: loadcourses - loads courses from json file
def loadcourses():
    with open("projcourses.json", "r") as myfile:
        Course.allcourses = json.load(myfile, object_hook=course_decoder)
    return 

#FUNCTION: loadstudents - loads students from json file
def loadstudents():
    from student import Student
    with open("projstudents.json") as myfile:
        Student.allstudents = json.load(myfile, object_hook=student_decoder)
    return 

#FUNCTION: login - logging a student to registeration system
def login():
    from student import Student
    print("Hello, welcome to the students' courses registration system")
    while True:
        id = input("Please enter student ID (001 to 029 (or 777 - this is a bonus student)) or type 'exit' to exit the program: ")
        if(id == "exit"):
            return False
        print()
        for student in Student.allstudents:
            if(id == student.ID):
                print(f"Hello, {student.name}")
                return student
        print("No such ID in the system's databse, please try again")
        continue
    
#FUNCTION: mainmenu - the main menu for the logged in student. the student chooses action for its account in the system:
#  1: display student
#  2: register to course 
#  3: remove course
#  4: display student's courses timetable
#  5: display student's exams
#  6: log off
#at the end of each action - updates json files of both courses and students
def mainmenu(student):
    while True:
        #load json files data
        loadcourses()
        loadstudents()
        #get command for student
        command = get_command(student.name)
        #proceeds to the action phase
        if command == str(MENU_ACTIONS.DISPLAY_STUDENT._value_):
            display_action(student)
            continue
        elif command == str(MENU_ACTIONS.REGISTER_COURSE._value_):
            register_action(student)
        elif command == str(MENU_ACTIONS.REMOVE_COURSE._value_):
            removal_action(student)
        elif command == str(MENU_ACTIONS.DISPLAY_TIMETABLE._value_):
            timetable_action(student)
        elif command == str(MENU_ACTIONS.DISPLAY_EXAMS._value_):
            exams_actions(student)
        elif command == str(MENU_ACTIONS.LOGOFF._value_):
            break
        else:
            print(Back.RED + "No such command")
            continue
        #update student's changes in allstudents -  global member of student class - using updatestudentlst
        student.updatestudentlst()
        #update json files
        update_students()
        update_courses()
    return

#FUNCTION: get_command - display the command options window and returns the typed command
def get_command(studentname):
    commandframe = '*'
    print(f"{commandframe*30}")
    print(Back.LIGHTCYAN_EX + f"{studentname}, choose your option:")
    command = input(f"1: Display {studentname}'s semester details\n2: Register to a course\n3: Remove a course from the {studentname}'s semester list\n4: Display {studentname}'s semester timetable (please extend the terminal window horizontally for propper display)\n5: Display {studentname}'s semester exams\n6: Logoff\n")
    return command

#FUNCTION: update course - update courses' changes to the related json file
def update_courses():
    with open("projcourses.json", "w") as myfile:
        json.dump(Course.allcourses, myfile, cls=CourseEncoder)
    return

#FUNCTION: update students - update students' changes to the related json file                
def update_students():
    from student import Student
    with open("projstudents.json", "w") as myfile:
        json.dump(Student.allstudents, myfile, cls=StudentEncoder)
    return

#FUNCTION: display_action - proceeds to display the student's details
def display_action(student):
    print (Back.YELLOW + 'Student Display')
    student.display_student()
    return

#FUNCTION: register_action - proceeds to a search action to find the course the student would like to register to
def register_action(student):
    print(Back.YELLOW + "Register a course")
    while True:
        #get results from searching courses
        results = search_action()
        #if there are any results, proceeds to a making a registration choice from the given number of results
        if results:
            #"choice" gets a number (int) from make_register_choice function given number of results or "exit" string
            choice = make_register_choice(results)
            #option to not register and return to the main menu
            if choice == "exit":
                break
            else:
                student.add_course(results[choice - 1])
                break
        else:
            continue
    return

#FUNCTION: make_register_choice - given matched courses from a search, asks the user to choose an course to registered to from the given matches
def make_register_choice(matches):
    while True:           
        choice = input("Type the result number (according to the results list) of the course you're intersted in, or type 'exit' to return to the main menu and not register at all: ")
        #option to exit registeration proccess
        if choice.lower() == "exit":
            break
        else:
            #tryexcept in case the user typed a non digit input other than exit
            try:
                resultnum = int(choice)
            except ValueError as ex:
                print(Back.RED + "Please type a number")
                continue
            else:
                #checks if the input number is NOT within total number of matches (example: a search session 3 matches, and user chooses result "5" or "-3")
                if (resultnum < 1) or (resultnum > len(matches)):
                    print(Back.RED + f"Please type a number within the results number range (1 to {len(matches)}) ")
                    continue
                else:
                    return resultnum
    return "exit"

#FUNCTION: search_action - recieves a desired search action - 1. by name, 2. by course number 3. by course points 4. by days 5. display all courses
def search_action():
    while True:
        inp = ""
        searchtype = input(f"Type your desired search:\n1: Search course by name\n2: Search course by course number\n3: Search course by points\n4: Search course by day\n5: Search for ALL courses\nOr type 'exit' to return to the main menu\n")
        #option to exit the search proccess
        if searchtype.lower() == "exit":
            return False
        #proceeds to get an input if the user chose a valid search method
        elif searchtype == str(SEARCH_TYPES.SEARCH_BY_NAME._value_):
            inp = input("Enter the searched course name (this includes partial name): ")
        elif(searchtype == str(SEARCH_TYPES.SEARCH_BY_NUM._value_)):
            inp = input("Enter the searched course number (this includes partial number): ")
        elif(searchtype == str(SEARCH_TYPES.SEARCH_BY_POINTS._value_)):
            inp = input("Enter the number of points you're looking for in the range 3 to 5: ")
        elif(searchtype == str(SEARCH_TYPES.SEARCH_BY_DAYS._value_)):
            inp = input("Enter the day you want to seacrh for (this includes partial name of the day): ")
        elif(searchtype == str(SEARCH_TYPES.SEARCH_ALL_COURSES._value_)):
            break
        #if the user typed invalid search method, notify him and continue the while loop
        else:
            print(Back.RED + "Invalid input, try again (enter a value between 1 to 5), or type 'exit' to return to main menu: ")
            continue
        #checks if the user typed a valid input in the given search method
        if(is_valid_input(inp, searchtype)):
                break
        else:
            continue
    res = Course.seacrh_course(inp, searchtype)
    return res

#FUNCTION: is_valid_input - using regular expression, checks if the input matches the search method
def is_valid_input(input, searchtype):
    #search by name - any comnination of words and numbers allowed
    if searchtype ==  str(SEARCH_TYPES.SEARCH_BY_NAME._value_):
        match = re.match(r"(^[A-Za-z0-9 _]*[A-Za-z0-9][A-Za-z0-9 _]*$)", input)
        if match:
            return True
        else:
            print(Back.LIGHTRED_EX + "You chose to search by name - Please type only letters and numbers (space inbetween - optional)")
    #search by number - only numbers allowed
    elif searchtype == str(SEARCH_TYPES.SEARCH_BY_NUM._value_):
        match = re.match(r"^[0-9]+$", input)
        if match:
            return True
        else:
            print(Back.LIGHTRED_EX + "You chose to search by number - Please type only numbers")
            return False
    #search by points - only numbers X or X.5 in the range 3 to 5 allowed
    elif searchtype == str(SEARCH_TYPES.SEARCH_BY_POINTS._value_):
        match = re.match(r"(^[3-5]\.*5*$)", input)
        if match:
            #dealing with the "5.5" points issue
            if match.groups()[0] == "5.5":
                print(Back.LIGHTRED_EX + "You chose to search by points - Please type only number X or X.5 in the range 3 to 5")
                return False
            else:
                return True
        else:
            print(Back.LIGHTRED_EX + "You chose to search by points - Please type only number X or X.5 in the range 3 to 5")
            return False
    #search by days - only letters allowed
    elif searchtype == str(SEARCH_TYPES.SEARCH_BY_DAYS._value_):
        match = re.match(r"(^[a-zA-Z]+$)", input)
        if match:
            return True
        else:
            print(Back.LIGHTRED_EX + "You chose to search by days - Please type only letters")
            return False

       
#FUNCTION: removal_action - proceeds to remove a course
def removal_action(student):
    print(Back.YELLOW + "Course removal")
    student.removecourse()
    return

#FUNCTION: timetable_action - proceeds to print student's timetable
def timetable_action(student):
    print(Back.YELLOW + "Timetable")
    print(Back.LIGHTCYAN_EX +"Legend: L = Lecture , T = Tutorial")
    student.print_timetable()
    return

#FUNCTION: exam_actions - proceeds to print student's exams
def exams_actions(student):
    print(Back.YELLOW + "Exams")
    student.print_exams()
    return

#FUNCTION: lessondetails - returns for a course a list of all lessons data 
def lessondetails(course):

    def splitdaysandhours(lesson):
        instance = []
        splitdayhours = lesson.split(" , ")
        day = splitdayhours[0]
        instance.append(day)
        hoursrange = splitdayhours[1].split(" - ")
        starthour = hoursrange[0]
        instance.append(starthour)
        endhour = hoursrange[1]
        instance.append(endhour)
        return instance

    res = []
    lecturestimes = course.timeLectures.split(" ; ")
    for item in lecturestimes:
        lecturedet = splitdaysandhours(item)
        lecturedet.append("L")
        res.append(lecturedet)
    tutorialtimes = course.timeTutorial.split(" ; ")
    for item in tutorialtimes:
        Tutordet = splitdaysandhours(item)
        Tutordet.append("T")
        res.append(Tutordet)
    return res

#FUNCTION: build_title - builds days title for timetable
def build_title():
    title = []
    boxoutline = "|"
    boxspace = " "
    lenbox = 30
    for i in range(5):
        if i == 0:
            word = "Sunday"
        elif i == 1:
            word = "Monday"
        elif i == 2:
            word = "Tuesday"
        elif i == 3:
            word = "Wednesday"
        elif i == 4:
            word = "Thursday"
        lenword = len(word)
        #create a day title box and put the day in the middle of the box
        box = boxoutline + boxspace*((lenbox - lenword)//2) + word + boxspace*((lenbox - lenword)//2)
        title.append(box)
    for item in title:
            # print(item, end="")
            print(Back.GREEN + item, end="")
    print("\n")