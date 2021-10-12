from student import *
from Test import *

test1 = Test()
test1.populate_test()

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
