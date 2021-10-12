class Student:
    def __init__(self, name):
        self.score = 0
        if self.valid_name(name):
            self.name = self.valid_name(name)
        else:
            self.name = None
            print("invalid name, try again")
            return

    def valid_name(self, name):
        if name.isdigit():
            return None
        return name
