
from faker import Faker
import string
import random
fake = Faker()

url = 'https://conduit.mate.academy/'
error_message_username = 'Username must start with a letter, have no spaces, and be 3 - 40 characters.'
error_message_already_taken_username = 'This username is taken.'
already_taken_username = {'testqan', 'compress390', 'regional557', 'new22', 'front-end483', 'architecture554', 'dewayne_anderson'}
random_username = random.choice(list(already_taken_username))
already_taken_email = {'test@test.test', 'test@test.test', 'test@test.com', 'test@test.com', 'testo@test.test'}
random_email = random.choice(list(already_taken_email))

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

def generate_short_username():
    username_length = 2 if random.randint(0, 1) == 0 else 1
    first_letter = random.choice(string.ascii_letters)
    if username_length == 2:
        second_char = random.choice(string.ascii_letters)
        return first_letter + second_char
    else:
        second_char = random.choice(string.digits)
        return first_letter + str(second_char)

def generate_long_username():
    username_length = random.randint(41, 50)
    first_letter = random.choice(string.ascii_lowercase)
    username_body = ''.join(random.choices(string.ascii_lowercase + string.digits, k=username_length-1))
    return first_letter + username_body
