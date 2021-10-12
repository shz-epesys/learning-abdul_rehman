import random

class Question:
    def __init__(self, question, option, answer):
        self.question = question
        self.option = option
        self.answer = answer


class Test:
    def __init__(self):
        self.students = []
        self.question_list = []
        self.qs = []

    def attempt_quiz(self, student):
        qs = shuffle(self.qs)
        print("Choose the right option of the given question:")
        for question in qs:
            answer = question_and_input(question)
            if answer is None:
                self.students.append(student)
                return
            if question.answer == answer:
                student.score += 1
        student.score = round(100*(int(student.score)/int(len(qs))), 3)
        self.students.append(student)
        self.display_students()

    def display_students(self):
        for std in self.students:
            print(
                f"Students who attempted the quiz are : {std.name}\n with final score of {std.score}%")

    def is_student_exist(self, student):
        list1 = list(filter(lambda entry: entry.name.lower() ==
                     student.name.lower(), self.students))
        if len(list1) > 0:

            return True
        else:
            return False

    def populate_test(self):

        no_of_questons = int(input("Enter the number of question in this :"))
        quest_dic = {}
        keys = ["question", "option", "answer"]

        for q in range(no_of_questons):
            question = input("Write the question:")
            print("Write four options to you question, below: ")
            options = list(input() for _ in range(4))

            answer = input("Provide correct answer from the given options:")
            values = [question, options, answer]
            quest_dic = {k: v for (k, v) in zip(keys, values)}
            self.question_list.append(quest_dic)
        self.qs = [
            Question(
                question=q["question"],
                option=q["option"],
                answer=q["answer"],
            )
            for q in self.question_list
        ]


def question_and_input(qs):
    print("\n" + qs.question + "\n")
    options = shuffle(qs.option)
    for index, option in enumerate(options):
        if option:
            print(f"{index} ) {option}")
    answer = None
    for x in range(0, 3):
        try:
            answer = int(input("\nanswer:"))
        except Exception:
            print("invalid entry,Enter a numeral")
        if answer not in range(len(options)):
            print("Invalid input, Try again")
        else:
            break
    if answer not in range(len(options)):
        print("You Fail")
        # exit()
        return
    return options[answer]


def shuffle(list):
    return random.sample(list, len(list))
