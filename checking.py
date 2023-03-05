import os

def register():
    while True:
        nameID = str(input("Enter your name: ")).lower()
        path = "faces/" + nameID
        isExist = os.path.exists(path)
        if isExist:
            print("Already Exist")
            pass
        else:
            os.makedirs(path)
            return nameID
            break

def login():
    while True:
        nameID = str(input("Enter your name: ")).lower()
        path = "faces/" + nameID
        isExist = os.path.exists(path)
        if isExist:
            print("You are logging.......")
            return nameID
            break
        else:
            print("Doesn't Exist")
            pass