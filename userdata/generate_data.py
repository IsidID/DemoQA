from faker import Faker
import string
import random
fake = Faker()


def generate_password():
    password_length = 8

    while True:
        password = fake.password(length=password_length,
                                 special_chars=True, digits=True, upper_case=True,
                                 lower_case=True)
        if (password[0].isalpha() and
                any(char.isdigit() for char in password) and
                any(char.isupper() for char in password) and
                any(char in string.punctuation for char in password)):
            return password



def generate_user_credentials():
    username = fake.user_name()
    email = fake.email()

    return {'username': username, 'email': email}