import pyperclip
import rsa
import csv
import ast



def handle_password_save():
    app = input("Write an app/website for which you want to save your password: ")
    password = input(f"Write the password for {app}: ")

    publicKey,privateKey = rsa.newkeys(512)

    encrypted_message = rsa.encrypt(password.encode(),publicKey)
    
    print(f"Your password is saved as: {app}|{password}")
    print("The private key was stored in current directory")

    with open(f"{app}_private_key.pem","wb") as file:
       file.write(privateKey.save_pkcs1()) 


    with open("passwords.csv", "a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows([[app,encrypted_message]])



def decrypt_password(app,encrypted_password):
    with open(f"{app}_private_key.pem", "rb") as file:
        private_key = rsa.PrivateKey.load_pkcs1(file.read())

    decrypted_password = rsa.decrypt(encrypted_password,private_key).decode()

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
                decrypt_password(row[0],ast.literal_eval(row[1]))
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


def main():

    while True:
        choise = input("\nWelcome to the password saving agent!\n"
        "1.Set new password 2.Print all saved passwords 3.Show password 4.Exit\n")

        try:
            choise = int(choise)

        except ValueError:
            print("write a number!!!!")


        if choise == 4:
            break
        elif choise == 1:
            handle_password_save()
        elif choise == 2:
            print_all_passwords()
        elif choise == 3:
            show_password()


if __name__ == "__main__":
    main()
