import pyperclip
import rsa
import csv
import ast
from getpass import getpass
import os
import bcrypt


def handle_key_generation():
    publicKey,privateKey = rsa.newkeys(512)
    
    with open("private.pem","wb") as private:
        private.write(privateKey.save_pkcs1())

    with open("public.pem","wb") as private:
        private.write(publicKey.save_pkcs1())
    
    print("New public and private keys were created in current directory")


def handle_password_save():
    found_same = False
    app = input("Write an app/website for which you want to save your password: ")
    
    with open("passwords.csv", "r") as file:
        password_csv_reader = csv.reader(file)
        for row in password_csv_reader:
            if len(row) < 2:
                continue

            if row[0] == app:
                found_same = True
                choice = input(f"You already have a password saved for {app}\n"
                    "1.Override current password 2.Create a password for new app/website 3. Cancel\n")
                try:
                    choice = int(choice)

                except ValueError:
                    print("Write a number!!!!")

                if choice == 2:
                    handle_password_save()
                elif choice == 1:
                    override_password(app)
                elif choice == 3:
                    break

    if not found_same:
        password = getpass(f"Write the password for {app}: ")

        with open(f"public.pem", "rb") as file:
            publicKey = rsa.PublicKey.load_pkcs1(file.read())

        encrypted_message = rsa.encrypt(password.encode(),publicKey)

        print(f"Your password for {app} was saved successfully")


        with open("passwords.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([[app,encrypted_message]])



def override_password(app):
    password = getpass(f"Write the new password for {app}: ")
    rows = []
    with open(f"public.pem", "rb") as file:
        publicKey = rsa.PublicKey.load_pkcs1(file.read())

    encrypted_message = rsa.encrypt(password.encode(),publicKey)
    print(f"Your password for {app} was saved successfully")

    with open("passwords.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) < 2:
                continue
            if row[0] == app:
                row[1] = encrypted_message
            rows.append(row)

    with open("passwords.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)



def decrypt_password(encrypted_password):
    with open(f"private.pem", "rb") as file:
        privateKey = rsa.PrivateKey.load_pkcs1(file.read())

    decrypted_password = rsa.decrypt(encrypted_password,privateKey).decode()

    print("Your password was coppied to clipboard")
    pyperclip.copy(decrypted_password)




def show_password():
    found = False
    app = input("Write an app/webiste for which you have saved a password: ")

    with open("passwords.csv", "r") as csvfile:
        password_csv_reader = csv.reader(csvfile)

        for row in password_csv_reader:
            if len(row) < 2:
                continue
            if row[0] == app:
                decrypt_password(ast.literal_eval(row[1]))
                found = True

    if not found:
        print("Unfortunately, there was no website/app with this name, maybe you misspelled it?\n"
            f"Your input was: {app}")


def print_all_passwords():

    with open("passwords.csv", "r") as csvfile:
        password_csv_reader = csv.reader(csvfile)
        for row in password_csv_reader:
            if len(row) < 2:
                continue
            else:
                print(f"\n{row[0]} | {row[1]}")

def main_loop():
    while True:
        choice = input("\nWelcome to the password saving agent!\n"
        "1.Set new password 2.Print all saved passwords 3.Show password 4.Exit\n")

        try:
            choice = int(choice)

        except ValueError:
            print("write a number!!!!")


        if choice == 4:
            break
        elif choice == 1:
            handle_password_save()
        elif choice == 2:
            print_all_passwords()
        elif choice == 3:
            show_password()

def generate_master_password():
    password = getpass("Create a new password: ").encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password,salt)
    repeat = getpass("Repeat your password: ").encode("utf-8")

    if bcrypt.checkpw(repeat,hashed):
        print("Your password was saved successfully!")
        
        with open("master_password.dat","wb") as file:
            file.write(hashed)

    else:
        print("Incorrect password, try again\n")
        generate_master_password()


def ask_master_password():
    password = getpass("Password: ").encode("utf-8")
    with open("master_password.dat","rb") as file:
        hashed = file.read()
        if bcrypt.checkpw(password,hashed):
            main_loop()
        else:
            print("Incorrect password")
            ask_master_password()


def main():

    directory = os.listdir(path=".")

    if "master_password.dat" not in directory:
        generate_master_password()

    if "private.pem" and "public.pem" not in directory:
        handle_key_generation()
    elif "private.pem" not in directory:
        print("Your private key is missing from program directory,\n"
            "either delete your public key to generate the new one or put you private key in program directory")
        quit()
    elif "public.pem" not in directory:
        print("Your public key is missing from program directory, \n"
            "either delete your public key to generate the new one or put you private key in program directory")
        quit()

    else:
        ask_master_password()
        quit()

    ask_master_password()

if __name__ == "__main__":
    main()
