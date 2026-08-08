import rsa
import pyperclip
import csv
from getpass import getpass


def handle_key_generation():
    publicKey,privateKey = rsa.newkeys(512)
    
    with open("data/private.pem","wb") as private:
        private.write(privateKey.save_pkcs1())

    with open("data/public.pem","wb") as private:
        private.write(publicKey.save_pkcs1())
    
    print("New public and private keys were created in current directory")



def handle_password_save():
    found_same = False
    app = input("Write an app/website for which you want to save your password: ").strip().lower()
    
    with open("data/passwords.csv", "r") as file:
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

        with open(f"data/public.pem", "rb") as file:
            publicKey = rsa.PublicKey.load_pkcs1(file.read())

        encrypted_message = rsa.encrypt(password.encode(),publicKey)

        print(f"Your password for {app} was saved successfully")


        with open("data/passwords.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([[app,encrypted_message]])



def override_password(app):
    password = getpass(f"Write the new password for {app}: ")
    rows = []
    with open(f"data/public.pem", "rb") as file:
        publicKey = rsa.PublicKey.load_pkcs1(file.read())

    encrypted_message = rsa.encrypt(password.encode(),publicKey)
    print(f"Your password for {app} was saved successfully")

    with open("data/passwords.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) < 2:
                continue
            if row[0] == app:
                row[1] = encrypted_message
            rows.append(row)

    with open("data/passwords.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)



def decrypt_password(encrypted_password):
    with open(f"data/private.pem", "rb") as file:
        privateKey = rsa.PrivateKey.load_pkcs1(file.read())

    decrypted_password = rsa.decrypt(encrypted_password,privateKey).decode()

    print("Your password was coppied to clipboard")
    pyperclip.copy(decrypted_password)


