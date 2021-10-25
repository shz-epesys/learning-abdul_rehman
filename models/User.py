from flask_sqlalchemy import SQLAlchemy
import re
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(60))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60),  nullable=False)
    contact_no = db.Column(db.String(13))
    address = db.Column(db.String(100))
    city = db.Column(db.String(20))

    def __init__(self, username, email, password, first_name, last_name, contact_no,  address, city):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.email = email
        self.contact_no = contact_no
        self.address = address
        self.city = city

    def validate_email(self):
        email = self.email
        pattern1 = r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$"
        # pattern1 = r"[0-9a-zA-Z_-]+@[a-zA-Z]+\.[a-zA-Z]"
        pattern = re.compile(pattern1)
        if not re.match(pattern, email):
            return False, 'Email format is not correct.'
        elif not email:
            return False,"No Entry"
        else:
            return True,"valid email"

    def validate_password(self):
        password = self.password
        # pattern3 = r"[+]?\d{3,5}[-., ]?\d{3}[-., ]?\d{4}"
        pattern3 = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[@#$%^&+=])[A-Za-z0-9@#$%^&+=]{8,}$'
        pattern = re.compile(pattern3)

        if not re.match(pattern, password):
            return False,"invalid password"
        elif not password:
            return False,"No Entry"
        else:
            return True,"Valid password"

    def validate_number(self):
        number = self.contact_no
        pattern2 = r"[+]?\d{3,5}[-., ]?\d{3}[-., ]?\d{4}"
        pattern = re.compile(pattern2)

        if not re.match(pattern, number):
            return False,"invalid number"
        elif not number:
            return False,"No Entry"
        else:
            return True,"Valid Number"


    def validate(self):
        status,message =self.validate_email()
        if not status:
            return False,message
        status,message =self.validate_password()
        if not status:
            return False, message
        status,message =self.validate_number()
        if not status:
            return False, message

        return True, 'All formats are correct.'