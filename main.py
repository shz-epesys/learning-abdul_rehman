# TASK:2)
# Our Learning management system needs functionality you implemented in task 1, so we can record each student's progress from our learning platform.
# HOW TO SOLVE)
# Create a Test Class which contains an empty list.
# Take inputs from the teacher and populate the list of dictionaries in Test Class.
# Generate a Test for a student with suffled questions and shuffled choices.
# Take answers from a student and store them in each dictionary of a list.
# Provide that list to a function of Test class to give a score to a Student.
import random
from student import Student
# from data import questions




if __name__ == '__main__':
    test1 = Test()
    test1.populate_test()
    # print(Test1.question_list)
    # test1 = Test()
    while 1:
        student = Student(input("Enter your Name:"))
        if student.name is None:
            del student
            continue
        if not test1.is_student_exist(student):
            test1.attempt_quiz(student, )
        else:
            print(
                f"you alreay attempted the test.")
            del student
