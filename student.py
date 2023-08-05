from datetime import datetime
from utils import lessondetails, build_title
from course import Course
from colorama import Back, init
#ensures colored prints using "colorama" package will reset automatically afterwards
init(autoreset=True)

#class Student revolves around the student attributes and methods

class Student:
    #defining a global member - list of all student objects
    allstudents = []
    #FUNCTION: __init__ - initialize attributes for student object - student name(name), student ID(ID), and a list of student's registered courses (courselst)
    def __init__(self, name, ID, courselst):
        self.name = name
        self.ID = ID
        self.courselst = courselst
        #appends the student object to the global member allstudents
        Student.allstudents.append(self)
        return
    
    #FUNCTION: check_course: checks if the wanted course does not collides with one or more of the already registered courses' lessons hours 
    def check_course(self, wantedcourse):
        #defining a flag - match - to mark a collision issue
        match = 0 
        #defining a list for future collisions
        overlaps = []
        #lesson details - function defined in utils.py which returns for a course a list of all lessons data  
        wantedetails = lessondetails(wantedcourse)
        #going through all student's current registered courses
        for course in self.courselst:
            timedet = lessondetails(course)
            #for each lesson of course (lecture #1, lecture #2, tutorial #1... etc. ) - checks if one of the wanted course's lesson collides
            for presentlesson in timedet:
                for requiredlesson in wantedetails:
                    #for the same day - checks if one of the wanted course's lessons ends in the middle of one of the present courses' lessons **OR** if one of the wanted course's lessons starts in the middle of one of the present courses' lesson
                    if(presentlesson[Course.COURSE_DETAILS.LESSON_DAY._value_] == requiredlesson[Course.COURSE_DETAILS.LESSON_DAY._value_]) and (((requiredlesson[Course.COURSE_DETAILS.LESSON_END_HOUR._value_] > presentlesson[Course.COURSE_DETAILS.LESSON_START_HOUR._value_]) and (requiredlesson[Course.COURSE_DETAILS.LESSON_END_HOUR._value_] <= presentlesson [Course.COURSE_DETAILS.LESSON_END_HOUR._value_])) or ((requiredlesson[Course.COURSE_DETAILS.LESSON_START_HOUR._value_] >= presentlesson [Course.COURSE_DETAILS.LESSON_START_HOUR._value_]) and (requiredlesson[Course.COURSE_DETAILS.LESSON_START_HOUR._value_] < presentlesson [Course.COURSE_DETAILS.LESSON_END_HOUR._value_]))):
                        match = 1
                        overlaps.append([course, presentlesson[Course.COURSE_DETAILS.LESSON_DAY._value_]])
        if match == 1:
            print (Back.RED + f"Desired course {wantedcourse.name} cannot be assigned to the student beacause it overlaps with the following registered courses days:\n")
            for item in overlaps:
                print(Back.LIGHTRED_EX+ f"{item[0].name}, {item[1]}")
            #collision - return False
            return False
        else:
            #no collision - return True
            return True
        
    #FUNCTION: add_course - adds the wanted course to the student's registered courses list if conditions are valid (1. the course is not already in the list 2. the course is not fulll and 3. the wanted course does not overlaps with another registered course in the list) 
    def add_course(self, wantedcourse):
        #checks if the wanted course is not already in the student's list - if so return without add the course again
        for item in self.courselst:
            if(wantedcourse.name == item.name):
                print(Back.RED + f"{self.name} is already registered to {wantedcourse.name}")
                return
        else:
            #checks if the wanted course is not fulll and the wanted course does not overlaps with another registered course in the list
            if (self.check_course(wantedcourse) and wantedcourse.check_open()):
                    self.courselst.append(wantedcourse)
                    wantedcourse.add_student(self)
                    print(Back.LIGHTGREEN_EX + f"{self.name} has successfully registered to {wantedcourse.name}")
            #if the wanted course does colide or overlaps with existing course - proceed without adding the wanted course
            else:
                pass
        return
    
    #FUNCTION: removecourse - displays all student's currently registered courses, the student can type a course name/number from the list and remove that course from his list
    def removecourse(self):
        self.print_courses()
        while True:
            inp = input("Enter the course name/number you want to remove (or type 'exit' to return to the main menu): ")
            #option to exit without removing anything
            if (inp.lower() == "exit"):
                return
            #removes the desired course - the input has to be the exact course number or the exact course name
            for course in self.courselst:
                if (course.name.lower() == inp.lower()) or (course.num == inp):
                    self.courselst.remove(course)
                    course.remove_student(self)
                    print (Back.LIGHTGREEN_EX + f"The course {course.name} has been removed from {self.name}'s courses list, here is the updated list")
                    self.print_courses()
                    return
            #in case the student typed non existant name/number - notify him and continue the loop
            print(Back.RED + "No such course in the list, please try again or quit:\n")

    #FUNCTION: print_courses - prints the courses in student's courses list        
    def print_courses(self):
        for course in self.courselst:
            print (course)

    #FUNCTION: calc_stud_points - calculates the total number of student's upcoming semester points
    def calc_stud_points(self):
        totalpoints = 0
        for course in self.courselst:
            totalpoints += float(course.points)
        print("Total points for upcoming semester:" + Back.LIGHTCYAN_EX+ f"{totalpoints} points")
        return
    
    #FUNCTION: display_student - displays students details - name, id, total points, and currently registered courses
    def display_student(self):
        print(f"Name: {self.name}\nID: {self.ID}\n")
        self.calc_stud_points()
        print(f"Course list:\n")
        self.print_courses()
        return
    
    #FUNCTION: updatestudentlst - updates the global member allstudents with updated logged student's data (new course added, removed course ect..), this function is important for json export of the data
    def updatestudentlst(self):
        for student in Student.allstudents:
            if self.ID == student.ID:
                Student.allstudents[Student.allstudents.index(student)] = self
            else:
                pass
        return
    
    #FUNCTION: sort_lessons - sorts the lessons in student's registered courses by days - all lessons in sunday will be gathered to a list "sun", all lessons in monday will be gathered to a list "mon" and so on. returns a list of days(each day is list of lessons) 
    def sort_lessons(self):
        #initialize each day list
        sun = []
        mon = []
        tue = []
        wed = []
        thu = []
        #for each course orginize all courses' lessons data in a list using "lessondetails" function
        for course in self.courselst:
            lessons = lessondetails(course)
            #analyzing each lesson of the course
            for lesson in lessons:
                #append course name to the lesson for future use (timetable function)
                lesson.append(course.name)
                #checks what day does the lesson take place and adds it to the propper list
                if (lesson[Course.COURSE_DETAILS.LESSON_DAY._value_] == "Sunday"):
                    sun.append(lesson)
                elif (lesson[Course.COURSE_DETAILS.LESSON_DAY._value_] == "Monday"):
                    mon.append(lesson)
                elif (lesson[Course.COURSE_DETAILS.LESSON_DAY._value_] == "Tuesday"):
                    tue.append(lesson)
                elif (lesson[Course.COURSE_DETAILS.LESSON_DAY._value_] == "Wednesday"):
                    wed.append(lesson)
                elif (lesson[Course.COURSE_DETAILS.LESSON_DAY._value_] == "Thursday"):
                    thu.append(lesson)
        days = [sun, mon, tue, wed, thu]
        #sorting each day in the list above (each day is a list of lessons) by start hours of lessons - so each day will have a list of lessons in chronological order
        for day in days:
            day.sort(key=lambda x: x[Course.COURSE_DETAILS.LESSON_START_HOUR._value_])
        return days
    
    #FUNCTION: print_timetable - prints student's timetable (for project fixed data - all courses are ranged between 9:00 to 18:00 )
    def print_timetable(self):
        #get a list of days (sunday to thursday) where each day has all student's lessons in chronological order
        days = self.sort_lessons()
        #bulids timtable title - the days
        build_title()
        #define hour boxes asthetics
        boxoutline = "|"
        boxspace = " "
        lenbox = 30
        #fixed data of all courses has the following behavior -  all courses are ranged between 9:00 to 18:00. so timtable will be created by 10 hour boxes for each hour in the range
        for i in range(10):
            #initialize a row for current hour's future data (lessons)
            row = []
            #creates hour display
            hour = str(i+9) + ":00"
            #fix a singular issue of 9:00 - change it to "09:00" for future strings comparisons 
            if i < 1:
                hour = "0" + str(i+9) + ":00"
            #assamble hourline at the side of the timetable aka "-----9:00, "----10:00" etc
            hourline = "-"*lenbox*5 + hour +"\n"
            print(hourline)
            #create hour box row - going day by day (sunday to thursday in chronological order) and for the current hour check if current day iteration has a lesson within it (example - for hour 10:00 the student A has a lesson X in monday from 10:00-12:00), and displays it if so
            for day in days:
                course = ""
                lencourse = len(course)
                for lesson in day:
                    # looking at a present hour box - for example 11:00, checks if lesson starts before present hour and ends after presnt hour and if so - display it for the current hour box in the propper day (example - lesson X from 10:00 to 12:00)
                    if (lesson[Course.COURSE_DETAILS.LESSON_START_HOUR._value_] <= hour) and (hour < lesson[Course.COURSE_DETAILS.LESSON_END_HOUR._value_]):
                        course = lesson[Course.COURSE_DETAILS.LESSON_NAME._value_] + f", {lesson[Course.COURSE_DETAILS.LESSON_TYPE._value_]}"
                        lencourse = len(course)
                #astheticlly fits the lesson name so it will be displayed in the middle of the hour box 
                box = boxoutline + boxspace*((lenbox - lencourse)//2) + course + boxspace*((lenbox - lencourse)//2)
                #append current day lesson to the present hour row
                row.append(box)
            for item in row:
                #prints all lessons for the present hour row in the same line
                print(item, end="")
            print("\n")

    #FUNCTION: prints all students' exams using datetime package to propperly display dates    
    def print_exams(self):
        #initialize list of exams - list of lists
        exams = []
        for course in self.courselst:
            #creating a list of exam's data (from the data string) for term A and term B
            for termstr in course.exams:
                term = []
                #separate exam's string list of strings [*exam date string*, *exam hours string*, *exam type string(A or B)*]
                termlst = termstr.split(" ; ")
                #create the date format for current exam 
                date = datetime.strptime(termlst[Course.TERM_DETAILS.TERM_DATE._value_], "%d-%m-%Y")
                #build the final list of exam data - [*date in datetime format*,  *exam hours string*, *exam type string(A or B)*, *exam name*]
                term.append(date)
                term.append(termlst[Course.TERM_DETAILS.TERM_HOURS._value_])
                term.append(termlst[Course.TERM_DETAILS.TERM_TYPE._value_])
                term.append(course.name)
                #append exam's data list to total exams list
                exams.append(term)
        #sort exams by the date so it will be in chronological order
        exams.sort(key=lambda x: x[Course.TERM_DETAILS.TERM_DATE._value_])
        print(f"Student {self.name} has the following exams: \n")
        for exam in exams:
            print(f"{exam[Course.TERM_DETAILS.TERM_DATE._value_].strftime('%e %B, %Y')}: {exam[Course.TERM_DETAILS.TERM_COURSE_NAME._value_]}, term {exam[Course.TERM_DETAILS.TERM_TYPE._value_]}, hours: {exam[Course.TERM_DETAILS.TERM_HOURS._value_]}")
        return
    #__str__: print student name and id                   
    def __str__(self):
        return (f"{self.name} , {self.ID}")
