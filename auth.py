from getpass import getpass
import bcrypt
from main_functions import main_loop


def generate_master_password():
    password = getpass("Create a new password: ").encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password,salt)
    repeat = getpass("Repeat your password: ").encode("utf-8")

    if bcrypt.checkpw(repeat,hashed):
        print("Your password was saved successfully!")
        
        with open("data/master_password.dat","wb") as file:
            file.write(hashed)

    else:
        print("Incorrect password, try again\n")
        generate_master_password()


def ask_master_password():
    password = getpass("Password: ").encode("utf-8")
    with open("data/master_password.dat","rb") as file:
        hashed = file.read()
        if bcrypt.checkpw(password,hashed):
            main_loop()
        else:
            print("Incorrect password")
            ask_master_password()

