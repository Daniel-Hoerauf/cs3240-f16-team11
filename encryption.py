from Crypto.Hash import SHA256

def main():
    info = {}
    hashPass = ''
    while True:
        user_id = input("Enter a user-id: ")
        password = input("Enter a password: ")
        if password == "":
            break
        else:
            hashPass = SHA256.new(str.encode(password)).hexdigest()
            info[user_id] = hashPass

    while True:
        user_id = input("Login by entering a user-id: ")
        password = input("Login by entering a password: ")
        val = info.get(user_id)
        check = SHA256.new(str.encode(password)).hexdigest()
        if val == None:
            print("user not found")
        elif hashPass != check:
            print("login fails")
        elif hashPass == check:
            print("login succeeds")
            break

if __name__ == '__main__':
    main()
