import os
from auth import ask_master_password, generate_master_password
from cryption import handle_key_generation


def main():
    if not os.path.isdir("data"):
        os.mkdir("data")

    directory = os.listdir(path="./data/")

    if "master_password.dat" not in directory:
        generate_master_password()

    if "private.pem" not in directory and "public.pem" not in directory:
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
