#Validation list:
#First and last name, 2 - 13 letters long, check if letters, format cases
#Password, 8+ chars, 1 num, 1 cap letter
#Battletag, 4+ chars, only alphanumeric chars

import random

##firstName = input("Firstname: ")
##surname = input("Surname: ")
##battletag = input("Battletag: ")
##password = input("Password: ")
##passwordCheck = input("Check password: ")

def nameIsValid(name):
    length = len(name)
    lengthValid = False
    alphabeticOnly = False
    if length <= 12 and length >= 2:
        lengthValid = True
    if name.isalpha():
        alphabeticOnly = True
    if lengthValid and alphabeticOnly:
        return True
    else:
        return False

def formatName(name):
    name = name[0].upper() + name[1:].lower()
    return name

def passwordIsValid(password):
    length = len(password)
    lengthValid = False
    containsNumber = False
    containsCapital = False
    containsProhibitedChar = False
    prohibitedChars = [" ", "(", ")"]
    if length <= 20 and length >= 8:
        lengthValid = True
    for n in range(0,length):
        for m in prohibitedChars:
            if password[n] == m:
                containsProhibitedChar = True
        if password[n].isupper():
            containsCapital = True
        if password[n].isnumeric():
            containsNumber = True
    if containsNumber and containsCapital and lengthValid and not(containsProhibitedChar):
        return True
    else:
        return False

def battletagIsValid(battletag):
    length = len(battletag)
    lengthValid = False
    alphaNumeric = False
    if length >= 5 and length <= 15:
        lengthValid = True
    if battletag.isalnum():
        alphaNumeric = True
    if lengthValid and alphaNumeric:
        return True
    else:
        return False


def createUsername(firstName,surname):
    randomNumString = ''
    for n in range(0,4):
        randomNum = random.randint(0,9)
        randomNumString = randomNumString + str(randomNum)
    username = firstName[0] + surname[0:3] + randomNumString
    return username
    
##if nameIsValid(firstName):
##    firstName = formatName(firstName)
##    print("First name is valid")
##    print(firstName)
##else:
##    print("First name not valid")
##    
##if nameIsValid(surname):
##    surname = formatName(surname)
##    print("Surname is valid")
##    print(surname)
##else:
##    print("Surname not valid")
##    
##if passwordIsValid(password):
##    print("Password valid")
##else:
##    print("Password not valid")
##
##if battletagIsValid(battletag):
##    print("Battletag is valid")
##else:
##    print("Battletag not valid")
##
##username = createUsername(firstName,surname)
##print(username)


    
