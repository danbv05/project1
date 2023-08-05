from utils import *
#main program - load the courses, load the students, initiate login, and proccesses main menu according to logged student's decisions
loadcourses()
loadstudents()
student = login()
if(student):
    mainmenu(student)