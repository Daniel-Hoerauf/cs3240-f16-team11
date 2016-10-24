#Nirali Jantrania
#nj3bd

#Original:
# dict = {}
# while True:
#     userid = input("Enter a userid to store: ")
#     if len(userid) == 0:
#         break
#     password = input("Enter a password to store: ")
#     if len(password) == 0:
#         break
#     dict[userid] = password
#
# print(dict)
#
# while True:
#     userid2 = input("Enter userid to login")
#     password2 = input("Enter password to login")
#     if not dict.has_key(userid2):
#         print("user not found")
#     elif dict.get(userid2) != password2:
#         print("login fails")
#     else:
#         print("login succeeds")

#Using pycrypto

from Crypto.Hash import SHA256
dict = {}
while True:
    userid = input("Enter a userid to store: ")
    if len(userid) == 0:
        break
    password = input("Enter a password to store: ")
    if len(password) == 0:
        break
    dict[userid] = SHA256.new(str.encode(password)).hexdigest()

print(dict)



while True:
    userid2 = input("Enter userid to login: ")
    if len(userid2) == 0:
        break
    if userid2 not in dict:
        print("user not found")
    password2 = input("Enter password to login: ")
    if len(password2) ==0:
        break
    hashPassword = SHA256.new(str.encode(password2)).hexdigest()
    if userid2 not in dict:
        print("user not found")
    elif dict.get(userid2) != hashPassword:
        print("login fails")
    else:
        print("login succeeds")