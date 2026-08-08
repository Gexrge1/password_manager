import csv
import ast
from cryption import decrypt_password,handle_password_save


def show_password():
    found = False
    app = input("Write an app/webiste for which you have saved a password: ").strip().lower()

    with open("data/passwords.csv", "r") as csvfile:
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

    with open("data/passwords.csv", "r") as csvfile:
        password_csv_reader = csv.reader(csvfile)
        
        for row in password_csv_reader:
            if len(row) < 2:
                continue
            else:
                print(f"{row[0]}")



def delete_password():
    app = input("Write the app/webiste to delete: ").strip().lower()
    rows = []
    found = False

    with open("data/passwords.csv","r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row)<2:
                continue
            if row[0] == app:
                found = True
                continue
            rows.append(row)


    with open("data/passwords.csv","w") as file:
        writer = csv.writer(file)
        writer.writerows(rows)


    if found:
        print(f"The password for {app} was successfully deleted")
    else:
        print(f"There is no application/website with the name {app}")

def main_loop():
    while True:
        choice = input("\nWelcome to the password saving agent!\n"
        "1.Set new password 2.Print all saved passwords 3.Show password 4.Delete password 5.Exit\n")

        try:
            choice = int(choice)

        except ValueError:
            print("write a number!!!!")


        if choice == 5:
            break
        elif choice == 1:
            handle_password_save()
        elif choice == 2:
            print_all_passwords()
        elif choice == 3:
            show_password()
        elif choice == 4:
            delete_password()


