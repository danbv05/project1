from enum import Enum
from colorama import Back, init
#ensures colored prints using "colorama" package will reset automatically afterwards
init(autoreset=True)

#class Course revolves around the courses attributes and methods
class Course:
    #COURSE_DETAILS - Enum inheritted class for lessons parameters
    class COURSE_DETAILS(Enum):
        LESSON_DAY = 0
        LESSON_START_HOUR = 1
        LESSON_END_HOUR = 2
        LESSON_TYPE = 3
        LESSON_NAME = 4
    #TERM_DETAILS - Enum inheritted class for exams parameters
    class TERM_DETAILS(Enum):
        TERM_DATE = 0
        TERM_HOURS = 1
        TERM_TYPE = 2
        TERM_COURSE_NAME = 3
    #defining a global member - list of all course objects
    allcourses = []
    #FUNCTION: __init__ - initialize attributes for course object - coursename(name), course number(num), course points(points), lecture times (timelectures), tutorial times(timetutorials), course exams (exams), maximum student capacity (maxstud), and a list of enlisted students (enlistedstud)
    def __init__(self, name, num, points, timeLectures, timeTutorial, exams, maxstud, enlistedstud = []):
        self.name = name
        self.num = num
        self.points = points
        self.timeLectures = timeLectures
        self.timeTutorial = timeTutorial
        self.exams = exams
        self.maxstud = maxstud
        self.enlistedstud = enlistedstud
        #appends the course object to the global member allcourses
        Course.allcourses.append(self)
        return
    
    #FUNCTION: search_course - recieves a string input, and a searchtype value (in correlation to enum table) and procceds with the suitable search
    @staticmethod
    def seacrh_course(input, searchtype):
        from utils import SEARCH_TYPES
        #match - a flag for indicating a match for search
        match = 0
        res = []
        rescount = 0
        #search all courses if it was desired by user
        if searchtype == str(SEARCH_TYPES.SEARCH_ALL_COURSES._value_):
            match = 1
            for course in Course.allcourses:
                res.append(course)
                rescount += 1
        else:
            for item in Course.allcourses:
                #disable case-sensetive issues for non-digits characters
                name = item.name.lower()
                lectures = item.timeLectures.lower()
                tutorials = item.timeTutorial.lower()
                #enables partial search - if the input is located somewhere in course name - consider it a result
                if (name.find(input.lower()) >= 0) and (searchtype == str(SEARCH_TYPES.SEARCH_BY_NAME._value_)):
                    match = 1
                    res.append(item)
                    rescount +=1
                    continue
                #partial search for course number
                if (item.num.startswith(input)) and (searchtype == str(SEARCH_TYPES.SEARCH_BY_NUM._value_)):
                    match = 1
                    res.append(item)
                    rescount +=1
                    continue
                #partial search - lessons days 
                if ((lectures.find(input) >= 0) or (tutorials.find(input) >= 0)) and (searchtype == str(SEARCH_TYPES.SEARCH_BY_DAYS._value_)):
                    match = 1
                    res.append(item)
                    rescount +=1
                    continue
                #search by course points (not partial search)
                if (item.points == input) and (searchtype == str(SEARCH_TYPES.SEARCH_BY_POINTS._value_)):
                    match = 1
                    res.append(item)
                    rescount +=1
                    continue
        if match == 0:
            print(Back.RED + "No matches")
            return False
        else:
            print(Back.GREEN + f"Found {rescount} results")
            innercount = 1
            #in case of existing search results - printing results
            for result in res:
                print(Back.YELLOW + f"Result {innercount} out of {rescount}:")
                print(f"{result}\n")
                print(Back.LIGHTMAGENTA_EX + f"Current available slots for this course: {result.maxstud - len(result.enlistedstud)} out of {result.maxstud}")
                if (result.maxstud - len(result.enlistedstud)) == 0:
                    print(Back.RED + "COURSE IS FULL")
                print("\n")
                innercount += 1
        return res
    
    #FUNCTION: check_open - checks if desired course is not full
    def check_open(self):
        if (len(self.enlistedstud) < self.maxstud):
            return True
        else:
            print(Back.RED + f"Sorry, the course {self.name} is full - {self.maxstud} students are already registerd (maximum capacity for this course)")
            return False
        
    #FUNCTION: add_student - add a registered student (name + id) to the course's enlisted students list    
    def add_student(self, student):
        self.enlistedstud.append([student.name, student.ID])
        return
    
    #FUNCTION: remove student - remove a registered student from course's enlisted students list 
    def remove_student(self, student):
        student_details = [student.name, student.ID]
        self.enlistedstud.remove(student_details)
        #remove student from the course in global member allcourses
        for course in Course.allcourses:
            if course.num == self.num:
                course.enlistedstud.remove(student_details)
        return
    
    #FUNCTION: __str__ - prints course's name, number and hours
    def __str__(self):
        print(Back.LIGHTBLUE_EX + "#######")
        return (f"\nCourse name: {self.name}\n----\nCourse number: {self.num}\n----\nPoints: {self.points}\nHours:\n**Lectures:**\n{self.timeLectures}\n**Tutorials:**\n{self.timeTutorial}\n")
