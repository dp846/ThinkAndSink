from tkinter import *
import random
import time
import hashlib
import csv
import tkinter.scrolledtext as st
import string
from base64 import b16encode
from datetime import datetime
import winsound

#Login and registration ===================>

def login():
    log = Tk() #This creates a root window to display widgets on, specifically the login related entries.
    log.configure(bg = 'black') #This configures with reference to the window created above the background colour and sets it to black, a more suitable colour for my project design.
    log.minsize(500,500) #Sets a minimum size of 500x500 pixels for the login screen so it cannot be made smaller than this size for convenience purposes.

    
    def loginSubmitted(): #This function will be called when the Submit button is clicked on the login tkinter window. 
        loginUsername = username_entry.get() #These two lines will retrieve the current text inside each entry box.
        loginPassword = password_entry.get()

        hashObject = hashlib.sha1(loginPassword.encode()) #This created a hashed object of the loginPassword using the SHA1 hash.
        hashHexText = hashObject.hexdigest() #This retrieves the hashed text in hex form from the object created.
        loginPassword = hashHexText #This stores the hashed passworentered in the variable of the login password variable.
        
        # DB OBJECT
        mydb = mysql.connector.connect(
          host="userwebs.hallcross.org",
          user="wals7255",
          password="WxJM4z",
          database="wals7255"
        )
        mycursor = mydb.cursor()
        sql_display = "SELECT * FROM userDetails"
        mycursor.execute(sql_display)
        myresult = mycursor.fetchall()
        readCSV = myresult

##        detailsFile = open("details.csv","r") #Opens the details file from the same folder as this code document in read mode.
##        readCSV = csv.reader(detailsFile, delimiter=',') #This uses the csv library file and the reader method it contains to separate the details file with commas.
        
        detailsMatch = False #Creates a boolean variable that will be used to check if the details entered match a record in the details file. 
        lineCount = 0 #Creates an integer variable of lineCount that will be incremented for each line looped through in the file. 
        for row in readCSV: #Creates a for loop repeating for the number  of rows in the file. 
            if lineCount >= 0: #This checks if the line being read is the 2nd or greater, as the first line in the file contains the headings for the columns.
                if (loginUsername == row[0] or loginUsername == row[2]) and loginPassword == row[1]: #Checks if the entered username and hashed password match the stored 1st and 2nd element in the current row of the details file (representing username and password).
                    detailsMatch = True #Sets the boolean variable to true as the details match.
                    username = row[0] #This passes the username from the current row into a username variable so it can be used in the next window, mainMenu.
                    battletag = row[2] #This passes the battletag from the current row into a battletag variable so it can be used in the next window, mainMenu.
            lineCount += 1 #Increments the line count variable.
        if detailsMatch: #Checks if the details were found.
            log.destroy() #If they were, the login screen is destroyed.
            mainMenu(username,battletag) #The program is sent to the main menu procedure with the two arguments of username and battletag.
        else:
            label = Label(log, text = "Username or password is incorrect", bg = 'black',fg = 'red').pack() #This will display text under the entry boxes in red if the details entered weren't found.

##        detailsFile.close() #This closes the details file.
        
        

    title_font = ("Impact",30) #This creates a font to be used in the titles on each screen
    Label(log, text = "Think and Sink", font = title_font, fg = 'green', bg = 'black').pack() #This creates a label widget using the title font created with the title, Think and Sink
    Label(log, text = "==============", font = title_font, fg = 'green', bg = 'black').pack()
    
    username_entry = Entry(log, bg = 'black',fg = 'green',insertbackground = "green") #This creates an entry box on the created window for login.
    Label(log, text = "Username or Battletag: ",bg = 'black',fg = 'green').pack() #This packs a new label to the screen for the username.
    username_entry.pack() #This packs the username entry box to the screen below to username label.
    password_entry = Entry(log, show = "*", bg = 'black',fg = 'green',insertbackground = "green") #This creates an entry box on the created window for the login password, the show parameter means that the text being entered is not shown.
    Label(log, text = "Password: ",bg = 'black',fg = 'green').pack() #This packs a new label to the screen for the password.
    password_entry.pack() #This packs the password tkinter entry box created above to the login window. 

    #The submit button is created below which has parameters passing size properties, colours for the foreground and background and also the submitted method to be run when clicked on.
    Label(log, bg = 'black').pack() # This packs a blank label to the window to separate the entries and the submit button.
    Button(log, command = loginSubmitted, text = "Submit", relief = RIDGE, width = 20, height = 2, fg = "white", bg = "grey", bd = 4).pack() #This creates and packs a submit button
    Label(log, bg = 'black').pack()

    Label(log, text = "Quick login (play as a guest): ",bg = 'black',fg = 'green').pack()
    Button(log, command = lambda username="guest",battletag="GUEST":mainMenu(username,battletag), text = "Play without an account", relief = RIDGE, width = 20, height = 2, fg = "white", bg = "grey", bd = 4).pack() #This creates and packs a submit button
    
def register():
    reg = Tk() #This creates a root window to display widgets on, specifically the registration related entries.
    reg.configure(bg = 'black') #This configures with reference to the window created above the background colour and sets it to black, a more suitable colour for my project design.
    reg.minsize(500,500)
    
    def registrationSubmitted():
        firstName = firstname_entry.get() #These lines all retrieve the current data in each of the referenced entry widgets from the register window. 
        surname = surname_entry.get()
        battletag = battletag_entry.get()
        password = password_entry.get()
        passwordCheck = passwordcheck_entry.get()

        import validate #This imports my own Python file called validate so I can use its functions to validate the retreived entries. 

        #The lines below create strings of messages to display to the user if the details entered do not satisfy the requirements:
        firstNameInvalidText = "First name is invalid - it must be between 2 and 13 characters long and only contain letters."
        surnameInvalidText = "Surname is invalid - it must be between 2 and 13 characters long and only contain letters."
        passwordInvalidText = "Password is invalid - it must be between 8-20 characters, contain at least on capital and one number and not include any spaces or brackets."
        battletagInvalidText = "Battletag is invalid - it must be between 5 and 15 characters in length and contain alphanumeric characters only aA-zZ and 0-9."
        passwordsNotMatchText = "Passwords do not match"

        if validate.nameIsValid(firstName): #This checks that the first name is valid (all the validation functions either return True or False).
            firstName = validate.formatName(firstName) #Given that the first name is valid, it will now be put in the correct format.
            if validate.nameIsValid(surname): #This checks that the surname is valid.
                surname = validate.formatName(surname) #Given that the surname is valid, it will now be put in the correct format.
                username = validate.createUsername(firstName,surname) #This creates a username with the validated entries of firstName and surname.
                if validate.passwordIsValid(password): #This checks that the password is valid.
                    if validate.battletagIsValid(battletag): #This checks that the battletag is valid.
                        if password == passwordCheck: #Checks if the two passwords entered match one another.
                            reg.destroy() #Once the registration details have been confirmed, validated and saved, the register window is closed down.
                            
                            #Hash password using the same method in the login section.
                            hashObject = hashlib.sha1(password.encode())
                            hashHexText = hashObject.hexdigest()
                            password = hashHexText

##                            detailsFile = open("details.csv","a") #This opens the details file in append mode, as the program will need to write the new information to it without overwriting the whole document.
##                            detailsFile.write("\n" + username + "," + password + "," + battletag + "," + firstName + "," + surname) #Writes the validated details on a new line in the file.
##                            detailsFile.close() #Closes the file.

                            # DB OBJECT
                            mydb = mysql.connector.connect(
                              host="userwebs.hallcross.org",
                              user="wals7255",
                              password="WxJM4z",
                              database="wals7255"
                            )
                            mycursor = mydb.cursor()

                            # INSERT RECORDS
                            sql_insert = "INSERT INTO userDetails (username, password, battletag, firstName, surname) VALUES ('{}', '{}', '{}', '{}', '{}')".format(username, password, battletag, firstName, surname)
                            mycursor.execute(sql_insert)
                            mydb.commit()
                            

                            mainMenu(username,battletag) #Sends the code to the mainMenu procedure passing username and battletag as arguments just like in the login section.
                            
                        else:
                            label = Label(reg, text = passwordsNotMatchText, bg = 'black',fg = 'red').pack() #Outputs a label with the appropriate message given the details were not accepted.
                    else:
                        label = Label(reg, text = battletagInvalidText, bg = 'black',fg = 'red').pack() #Outputs a label with the appropriate message given the details were not accepted.
                else:
                    label = Label(reg, text = passwordInvalidText, bg = 'black',fg = 'red').pack() #Outputs a label with the appropriate message given the details were not accepted.
            else:
                label = Label(reg, text = surnameInvalidText, bg = 'black',fg = 'red').pack() #Outputs a label with the appropriate message given the details were not accepted.
        else:
            label = Label(reg, text = firstNameInvalidText, bg = 'black',fg = 'red').pack() #Outputs a label with the appropriate message given the details were not accepted.    

    title_font = ("Impact",30) #This creates a font to be used in the titles on each screen
    Label(reg, text = "Think and Sink", font = title_font, fg = 'green', bg = 'black').pack() #This creates a label widget using the title font created with the title, Think and Sink
    Label(reg, text = "==============", font = title_font, fg = 'green', bg = 'black').pack()

    #This makes a tiknter entry widget for each user detial that I require for their account creation.
    firstname_entry = Entry(reg, bg = 'black',fg = 'green',insertbackground = "green")
    surname_entry = Entry(reg, bg = 'black',fg = 'green',insertbackground = "green")
    battletag_entry = Entry(reg, bg = 'black',fg = 'green',insertbackground = "green")
    password_entry = Entry(reg, bg = 'black',fg = 'green', show = "*",insertbackground = "green")
    passwordcheck_entry = Entry(reg, bg = 'black',fg = 'green', show = "*",insertbackground = "green")

    #This will display each entry widget along with a corresponding label widget so a uer knows what to enter into each entry widget. 
    Label(reg, text = "First name: ", bg = 'black',fg = 'green').pack()
    firstname_entry.pack()
    Label(reg, text = "Surname: ", bg = 'black',fg = 'green').pack()
    surname_entry.pack()
    Label(reg, text = "Battletag: ", bg = 'black',fg = 'green').pack()
    battletag_entry.pack()
    Label(reg, text = "Password: ", bg = 'black',fg = 'green').pack()
    password_entry.pack()
    Label(reg, text = "Confirm password: ", bg = 'black',fg = 'green').pack()
    passwordcheck_entry.pack()

    Label(reg, bg = 'black').pack() # This packs a blank label to the window to separate the entries and the submit button.
    Button(reg, command = registrationSubmitted, text = "Submit", relief = RIDGE, width = 20, height = 2, fg = "white", bg = "grey", bd = 4).pack()
    
def startUp():
    menu = Tk() #Creates a root window
    menu.configure(bg = 'black')
    menu.minsize(500,500)
    title_font = ("Impact",30) #This creates a font to be used in the titles on each screen
    text_font = ("Courier",11)
    Label(menu, text = "Think and Sink", font = title_font, fg = 'green', bg = 'black').pack() #This creates a label widget using the title font created with the title, Think and Sink
    Label(menu, text = "==============", font = title_font, fg = 'green', bg = 'black').pack()

    #These lines will create buttons, and the parameters passed to it will style it and the command will trigger the login or register fucnction, depending on which is clicked
    Button(menu, command = login, text = "Login", relief = RIDGE, width = 40, height = 4, fg = "black", bg = "green", bd = 4).pack()
    Label(menu, bg = 'black').pack() # This packs a blank label to the window to separate the entries and the submit button.
    Button(menu, command = register, text = "Register", relief = RIDGE, width = 40, height = 4, fg = "black", bg = "green", bd = 4).pack()
    Label(menu, bg = 'black').pack()

    Label(menu, text = "Think and Sink v1.0.2", font = text_font, fg = 'green', bg = 'black').pack()
    Label(menu, text = "Created by Dan Parsley", font = text_font, fg = 'green', bg = 'black').pack()

    

    global musicOn
    musicOn = IntVar()

    menu.mainloop() #This method is called for an infinite loop to run the program

def mainMenu(username,battletag):

    def outputRules():

        file = open("rules.txt","r")
        for line in file:
            print(line)
        file.close()
        
    mainMenu = Tk() #Creates a root window for the main menu after log in.
    mainMenu.configure(bg = 'black')
    mainMenu.minsize(500,500)
    title_font = ("Impact",30) #This creates a font to be used in the titles on each screen
    Label(mainMenu, text = "Think and Sink", font = title_font, fg = 'green', bg = 'black').pack() #This creates a label widget using the title font created with the title, Think and Sink
    Label(mainMenu, text = "==============", font = title_font, fg = 'green', bg = 'black').pack()

    #These lines simply create 2 labels that will be packed to the menu screen welcoming the user. 
    welcomeText = "Welcome back " + battletag
    loggedInAsText = "You are logged in as " + username
    
    Label(mainMenu, text = welcomeText, fg = 'green', bg = 'black').pack()
    Label(mainMenu, text = loggedInAsText, fg = 'green', bg = 'black').pack()
    Label(mainMenu, bg = 'black').pack()


    #These lines will create buttons, and the parameters passed to it will style it.
    Button(mainMenu, text = "Regular Game - 2 Player", command = lambda username=username,battletag=battletag,onePlayer=False:gameTkinterVersion(username,battletag,onePlayer), relief = RIDGE, width = 40, height = 3, fg = "black", bg = "green", bd = 4).pack()
    Label(mainMenu, bg = 'black').pack() 
    Button(mainMenu, text = "Regular Game - Computer Opponent", command = lambda username=username,battletag=battletag,onePlayer=True:gameTkinterVersion(username,battletag,onePlayer), relief = RIDGE, width = 40, height = 3, fg = "black", bg = "green", bd = 4).pack()
    Label(mainMenu, bg = 'black').pack()
    Button(mainMenu, text = "Chaos Mode - 1 player", relief = RIDGE, width = 40, height = 3, fg = "black", bg = "green", bd = 4, command = lambda username=username,battletag=battletag:gameChaosMode(username,battletag)).pack()
    Label(mainMenu, bg = 'black').pack()
    Button(mainMenu, command = outputRules, text = "Display rules", relief = RIDGE, width = 40, height = 3, fg = "black", bg = "green", bd = 4).pack()
    Label(mainMenu, bg = 'black').pack()
    Button(mainMenu, command = lambda username=username,battletag=battletag:accountPage(username,battletag), text = "Your Account", relief = RIDGE, width = 40, height = 3, fg = "black", bg = "green", bd = 4).pack()
    Label(mainMenu, bg = 'black').pack()
    Button(mainMenu, command = lambda username=username,battletag=battletag:leaderboard(username,battletag), text = "Leaderboards", relief = RIDGE, width = 40, height = 3, fg = "black", bg = "green", bd = 4).pack()
    Label(mainMenu, bg = 'black').pack()
    Button(mainMenu, command = settings, text = "Settings", relief = RIDGE, width = 40, height = 3, fg = "black", bg = "green", bd = 4).pack()
    Label(mainMenu, bg = 'black').pack()

    
    #Colours:
    global col0
    global col1
    global col2
    global col3
    global col4
    global col5
    colourSet = ["red", "black", "green", "magenta4", "grey64", "lime"]
    col0 = colourSet[0]
    col1 = colourSet[1]
    col2 = colourSet[2]
    col3 = colourSet[3]
    col4 = colourSet[4]
    col5 = colourSet[5]

    mainMenu.mainloop() #This method is called for an infinite loop to run the window and update it with any changes.

#The account page (when selected in the menu as an option) will open and provide the user with their account statistics 
def accountPage(username,battletag):
    #Defining a new tkinter parent window along with some properties like a minimum size of 500 by 500 pixels and a olour of black. 
    accountPage = Tk()
    accountPage.configure(bg = 'black')
    accountPage.minsize(500,500)

    #Defining fonts:
    title_font = ("Impact",30)
    subtitle_font = ("Courier",22)
    text_font = ("Courier",18)
    
    Label(accountPage, text = "Think and Sink", font = title_font, fg = 'green', bg = 'black').pack() #This creates a label widget using the title font created with the title, Think and Sink
    Label(accountPage, text = "==============", font = title_font, fg = 'green', bg = 'black').pack()
    
    Label(accountPage, text = "Your latest game results:",font = subtitle_font, fg = 'green', bg = 'black').pack()
    Label(accountPage, bg = 'black').pack()

    outcomesFile = open("gameOutcomesRegular.csv","r") #Opening the file that holds info on game outcomes
    readCSV = csv.reader(outcomesFile, delimiter=',')

    arrayOfOutcomes = []
    
    for row in readCSV:
        line = []
        for value in row:
            line.append(value)    
        arrayOfOutcomes.append(line)

    outcomeCount = 0
    totalWins = 0
    totalLosses = 0
    totalGames = 0
    totalTurns = 0
    
    for row in reversed(arrayOfOutcomes):
        if outcomeCount < 10:
            if row[0] == username: #If user is the winner
                if row[2] == "0":
                    winningText = "WIN - " + battletag + " won against a human opponent in " + row[3] + "turns"
                    Label(accountPage, text = winningText, fg = 'green', bg = 'black').pack()
                else:
                    if row[2] == "1":
                        difficulty = "Easy"
                    elif row[2] == "2":
                        difficulty = "Medium"
                    else:
                        difficulty = "Hard"
                    winningText = "WIN - " + battletag + " won against an AI opponent of " + difficulty + " difficulty in " + row[3] + " turns"
                    Label(accountPage, text = winningText, fg = 'green', bg = 'black').pack()

                outcomeCount += 1
            elif row[1] == username:
                if row[2] == "0":
                    lossText = "LOSS - " + battletag + " lost to a human opponent in " + row[3] + "turns"
                    Label(accountPage, text = lossText, fg = 'red', bg = 'black').pack()
                else:
                    if row[2] == "1":
                        difficulty = "Easy"
                    elif row[2] == "2":
                        difficulty = "Medium"
                    else:
                        difficulty = "Hard"
                    lossText = "LOSS - " + battletag + " lost to an AI opponent of " + difficulty + " difficulty in " + row[3] + " turns"
                    Label(accountPage, text = lossText, fg = 'red', bg = 'black').pack()

                outcomeCount += 1

        if row[0] == username:
            totalWins += 1
            totalTurns += int(row[3])
        elif row[1] == username:
            totalLosses += 1
            totalTurns += int(row[4])

    totalGames = totalWins + totalLosses
    
    Label(accountPage, bg = 'black').pack()
    Label(accountPage, text = "Total number of games you have played: " + str(totalGames),font = text_font, fg = 'green', bg = 'black').pack()
    Label(accountPage, text = "Total number of games you have won: " + str(totalWins),font = text_font, fg = 'green', bg = 'black').pack()
    Label(accountPage, text = "Total number of turns you have had: " + str(totalTurns),font = text_font, fg = 'green', bg = 'black').pack()
        
    accountPage.mainloop()


def settings():
    settings = Toplevel()
    settings.configure(bg = 'black')
    settings.minsize(500,500)

    title_font = ("Impact",30) #This creates a font to be used in the titles on each screen
    subtitle_font = ("Courier",24)
    Label(settings, text = "Think and Sink", font = title_font, fg = 'green', bg = 'black').pack() #This creates a label widget using the title font created with the title, Think and Sink
    Label(settings, text = "==============", font = title_font, fg = 'green', bg = 'black').pack()
    Label(settings, text = "Settings", font = subtitle_font, fg = 'green', bg = 'black').pack()
    Label(settings, bg = 'black').pack()


    def updateColourblind(): #This updates the colourblind setting after the checkbutton is clicked on
        if colourblindOn.get() == 1:
            colourSet = ["red", "black", "yellow", "blue", "white", "lime"]
        else:
            colourSet = ["red", "black", "green", "magenta4", "grey64", "lime"]

        global col0
        global col1
        global col2
        global col3
        global col4
        global col5
        col0 = colourSet[0]
        col1 = colourSet[1]
        col2 = colourSet[2]
        col3 = colourSet[3]
        col4 = colourSet[4]
        col5 = colourSet[5]

    def updateMusic(): #This updates the music setting when the music button is clicked on
        if musicOn.get() == 1:
            winsound.PlaySound('menuSong.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
        else:
            winsound.PlaySound(None,winsound.SND_ASYNC)

    global musicOn
    musicOn = IntVar()
    checkMusic = Checkbutton(settings, text='Music on', variable=musicOn,fg = "black", bg = "green",  width = 40, height = 4, command = updateMusic)
    checkMusic.pack()
    
    Label(settings, bg = 'black').pack()
    
    colourblindOn = IntVar()
    checkColour = Checkbutton(settings, text='Colourblind mode', variable=colourblindOn,fg = "black", bg = "green",  width = 40, height = 4, command = updateColourblind)
    checkColour.pack()


#Leaderboard tab will open the chaos mode game results shown in a suitable leaderboard format that can be sorted by either fewest turns or quickest time. 
def leaderboard(username,battletag):
    #Defining a new tkinter parent window along with some properties like a minimum size of 500 by 500 pixels and a colour of black.
    try: #This will try the code indented below, so if it cannot connect to the database due to an internet connection error, the program will not crash
        leaderboard = Tk()
        leaderboard.configure(bg = 'black')

        frameTop = LabelFrame(leaderboard,bg = "black",borderwidth=0,highlightthickness=0)
        
        canvas = Canvas(leaderboard)
        scrollY = Scrollbar(leaderboard, orient="vertical", command=canvas.yview)

        frameBottom = LabelFrame(canvas,bg = "black",borderwidth=0,highlightthickness=0)

        

        #Defining fonts:
        title_font = ("Impact",30)
        subtitle_font = ("Courier",22)
        text_font = ("Courier",18)
        
        Label(frameTop, text = "Think and Sink", font = title_font, fg = 'green', bg = 'black').pack() #This creates a label widget using the title font created with the title, Think and Sink
        Label(frameTop, text = "==============", font = title_font, fg = 'green', bg = 'black').pack()

        Label(frameTop, text = "Click the TURNS or TIME (secs) buttons to sort by each!", fg = 'green', bg = 'black').pack()
        Label(frameTop, text = "Chaos Mode Leaderboard",font = subtitle_font, fg = 'green', bg = 'black').pack()
        
        def createLeaderboard(sortByIndex): #Parameter is 2 for numOfTurns, 3 for time
            
            if sortByIndex == 2:
                sortByTime = False
            else:
                sortByTime = True

            # DB OBJECT
            mydb = mysql.connector.connect(
              host="userwebs.hallcross.org",
              user="wals7255",
              password="WxJM4z",
              database="wals7255"
            )
            mycursor = mydb.cursor()
            sql_display = "SELECT * FROM gameOutcomes"
            mycursor.execute(sql_display)
            myresult = mycursor.fetchall()



            outcomes = myresult

            listOfValues = []
            resultsList = []
            lineNumber = 0
            leaderboardList = [["RANK","BATTLETAG","TURNS","TIME (secs)","USERNAME"]]
            record = []

            for row in outcomes:
                listOfValues.append(int(row[sortByIndex]))
                resultsList.append(row)

            

            listOfValues = sorted(listOfValues)
            rank = 1

            for time in listOfValues:
                timeFound = False
                for rowNum in range(0,len(resultsList)):
                    row = resultsList[rowNum]
                    if str(row[sortByIndex]) == str(time) and timeFound == False:
                        record = [str(rank),row[1],row[2],row[3],row[0]]
                        resultsList[rowNum] = ["","","",""]
                        timeFound = True
                leaderboardList.append(record)
                rank += 1
            
            #Displaying the leaderboard in an aesthetically pleasing manner with corresponding colours
            for record in range(0,len(leaderboardList)):
                for element in range (0,len(leaderboardList[record])):

                    subtitle_font = ("Courier",13)

                    button = Button(frameBottom,text=leaderboardList[record][element],bd=3,width=15,font=subtitle_font, relief=RIDGE, height=2,fg="white",bg="blue")
                    
                    if record == 0:
                        button["bg"] = "grey"
                        if element == 2:
                            button = Button(frameBottom,text=leaderboardList[record][element],bd=3,width=15,font=subtitle_font, relief=RIDGE, height=2,fg="white",bg="grey",command = lambda sortByIndex=2:createLeaderboard(sortByIndex))
                            if not(sortByTime):
                                button["bg"] = "green"
                                button["fg"] = "black"
                        if element == 3:
                            button = Button(frameBottom,text=leaderboardList[record][element],bd=3,width=15,font=subtitle_font, relief=RIDGE, height=2,fg="white",bg="grey",command = lambda sortByIndex=3:createLeaderboard(sortByIndex))
                            if sortByTime:
                                button["bg"] = "green"
                                button["fg"] = "black"
                
                    elif record == 1:
                        button["bg"] = "gold"
                        button["fg"] = "bisque4"
                        if element == 1:
                            button["text"] = "♕" + button["text"]
                            button["fg"] = "silver"
                    elif record == 2:
                        button["bg"] = "silver"
                        button["fg"] = "brown"
                    elif record == 3:
                        button["bg"] = "bisque4"
                        button["fg"] = "brown"
                    else:
                        button["fg"] = "white"
                    button.grid(row=record,column=element)
                    
        leaderboardList = createLeaderboard(2)
        sortedByTime = False

        canvas.create_window(0, 0, anchor='nw', window=frameBottom)
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'),yscrollcommand=scrollY.set)

        frameTop.grid(row=0,column=0)
        canvas.configure(width=800,height=500,bg="black")
        canvas.grid(row=1,column=0)
        scrollY.grid(sticky="ns",column=1,row=1)
        leaderboard.mainloop()
    except:
        print(" ==> Could not connect to database :(  ")



def quitGame(gameScreen): #This being called creates a pop up window that shows buttons to confirm a user wants to quit the game, yes or no options. 
    confirm = Tk()
    def respondYes(): #This destroys both the game window and the confirmation window when Yes is clicked
        gameScreen.destroy()
        confirm.destroy()
    def respondNo(): #This destroys the confirmation window and forces the game screen back onto the front focus on the screen. 
        confirm.destroy()
        gameScreen.focus_force()
    
    frameTop = LabelFrame(confirm,bg = backgroundCol,padx = 6,pady = 6,borderwidth=0,highlightthickness=0)
    frameBottom = LabelFrame(confirm,bg = backgroundCol,padx = 6,pady = 6,borderwidth=0,highlightthickness=0)
    confirm.configure(bg = backgroundCol)
    
    Label(frameTop,text="Are you sure you'd like to quit?", font = font2, height=2,fg=buttonCol,bg=backgroundCol).grid(row=0)
    yes = Button(frameBottom,text="Yes",bd=4, relief=RIDGE, font = font2, width=10, height=2,fg=backgroundCol,bg=buttonCol,command=respondYes)
    no = Button(frameBottom,text="No",bd=4, relief=RIDGE, font = font2, width=10, height=2,fg=backgroundCol,bg=buttonCol,command=respondNo)

    yes.grid(column=0,row=0)
    Label(frameBottom,width=10,bg=backgroundCol).grid(column=1,row=0)
    no.grid(column=2,row=0)
    frameTop.pack()
    frameBottom.pack()



# Below is the code for the function of the GUI version of regular battleships - whether it is against AI or not depends on the parameters passed in (onePlayer boolean)
def gameTkinterVersion(username,battletag,onePlayer):

    if musicOn.get() == 1:
        winsound.PlaySound('regularMode.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
    else:
        winsound.PlaySound(None,winsound.SND_ASYNC)
    
    #Number to letter conversions

    def numToLetter(num):
        num2alpha = dict(zip(range(1, 27), string.ascii_uppercase))
        letter = num2alpha[num]
        return letter

    def letterToNum(letter):
        letter = letter.upper()
        alpha2num = dict(zip(string.ascii_uppercase, range(1, 27)))
        num = alpha2num[letter]
        return num


    #Player class:

    class player:
        numOfTurns = 0
        username = ''
        battletag = ''
        ships = []
        humanPlayer = True
        shipGrid = [[]]
        guessingGrid = [[]]
        buttons = []

        def __init__(self,setUsername,setBattletag,setHumanPlayer,setShips,setShipGrid,setGuessingGrid,setButtons):
            self.username = setUsername
            self.battletag = setBattletag
            self.humanPlayer = setHumanPlayer
            self.ships = setShips
            self.shipGrid = setShipGrid
            self.guessingGrid = setGuessingGrid
            self.buttons = setButtons

    #Ship class:

    class ship:
        name = ''
        length = 0
        symbol = ''
        h_direction = 0 #1 right, -1 left
        v_direction = 0 #1 down, -1 up
        frontX = 0
        frontY = 0
        xCoords = []
        yCoords = []

        def __init__(self,setName,setSymbol,setLength,setHDirection,setVDirection,setFrontX,setFrontY,setXcoords,setYcoords):
            self.name = setName
            self.symbol = setSymbol
            self.length = setLength
            self.h_direction = setHDirection
            self.v_direction = setVDirection
            self.frontX = setFrontX
            self.frontY = setFrontY
            self.xCoords = setXcoords
            self.yCoords = setYcoords

    #Gameplay procedures

    def generateGrid(width): #Generates a blank grid of a specified width in the form of a 2d array
        grid = [["~"]*width for _ in range(width)]
        return grid

    def randomHdirection(): #Generates a directon to face horizontally for the ship (could also be created to be vertical in which case randomVdirection controls the direction)
        horizOrVert = random.randint(1,2) #1 for horizontal, 2 for vertical
        h_direction = 0
        if horizOrVert == 1:
            while h_direction == 0:
                h_direction = random.randint(-1,1)
        return h_direction

    def randomVdirection(h_direction): #Generates a random vertical direction for a ship, up or down.
        v_direction = random.randint(-1,1)
        if h_direction == 0:
            while v_direction == 0:
                v_direction = random.randint(-1,1)
        else:
            v_direction = 0
        return v_direction

    def createShips(): #Creates an array of ship objects.
        #setName,setSymbol,setLength,setHDirection,setVDirection,setX,setY,setXcoords,setYcoords
        
        carrier = ship("Aircraft carrier", "A",5,0,0,0,0,[],[])
        battleship = ship("Battleship", "B",4,0,0,0,0,[],[])
        submarine = ship("Submarine", "S",3,0,0,0,0,[],[])
        cruiser = ship("Cruiser", "C",3,0,0,0,0,[],[])
        destroyer = ship("Destroyer", "D",2,0,0,0,0,[],[])
        

        ships = [carrier, battleship, submarine, cruiser, destroyer]
        return ships



    def randomShipCoords(ship,grid,currentPlayer): #Generates random coordintes for ONE ship belonging to a player on a specified grid
        positionAvailable = False
        counter = 0
        while positionAvailable == False and counter <= 1000:

            positionAvailable = True
                
            ship.xCoords = []
            ship.yCoords = []

            horizontalDirection = randomHdirection()
            verticalDirection = randomVdirection(horizontalDirection)
            ship.h_direction = horizontalDirection
            ship.v_direction = verticalDirection

            rnd1 = random.randint(0,len(grid)-1)
            rnd2 = random.randint(0,len(grid)-1)
            ship.frontX = rnd1
            ship.frontY = rnd2
            
            XandYcoords(ship)

            for n in range (0,ship.length):
                x = int(ship.xCoords[n])
                y = int(ship.yCoords[n])
                gridWidth = len(grid) - 1
                if not(x > gridWidth or x < 0 or y > gridWidth or y < 0):
                    if grid[y][x] != "~" or currentPlayer.guessingGrid[y][x] == 'O' or currentPlayer.guessingGrid[y][x] == '#':
                        positionAvailable = False
                        counter += 1
                else:
                    positionAvailable = False
                    counter += 1
        if counter >= 200:
            return False
        else:
            return True

    def XandYcoords(ship): #Given a ship's X and Y front coordinate and direction, it will append the rest of the ships coords to the coordinate arrays for x and y.
        Xmultiplier = -(ship.h_direction)
        Ymultiplier = -(ship.v_direction)
        for i in range (0,ship.length):
            ship.yCoords.append(str(ship.frontY+(i*Ymultiplier)))
        for j in range (0,ship.length):
            ship.xCoords.append(str(ship.frontX+(j*Xmultiplier)))

    def shipOntoGrid(ship,grid): #Places a ship onto a grid by setting the correct index of the ship's x and y coordinates to its specific symbol in the grid 2d array.
        for n in range (0,ship.length):
            x = int(ship.xCoords[n])
            y = int(ship.yCoords[n])
            grid[y][x] = ship.symbol

    def displayGrid(grid): #Outputs an ASCII version of a specified grid, without tkinter buttons (used for debugging purposes)
        line = ""
        num = (len(grid)*2)+3
        outline = "   "
        topnumbers = "     "
        for x in range (1,len(grid)+1):
            col = numToLetter(x)
            topnumbers = topnumbers + col + " "
        print(topnumbers)
        for i in range(0,num):
            outline = outline + "-"
        print(outline)
        for y in range (0,len(grid)):
            for x in range (0,len(grid)):
                line = line + " " + grid[y][x]
            if len(str(y+1)) == 1:
                print(str(y+1) + "  ¦" + line + " ¦")
            else:
                print(str(y+1) + " ¦" + line + " ¦")
            line = ""
        print(outline)

    def removeIfSunk(player,opponent): #Loops through a player's ships and removes any that have been sunk, meaning there are none of its symbols in the grid that are left.
        for shipObj in opponent.ships:
            shipExists = False
            for y in range(0,len(opponent.guessingGrid)):
                for x in range(0,len(opponent.guessingGrid)):
                    if opponent.shipGrid[y][x] == shipObj.symbol:
                        shipExists = True
            if shipExists == False:
                for n in range(0,shipObj.length):
                    y = int(shipObj.yCoords[n])
                    x = int(shipObj.xCoords[n])
                    
                    player.guessingGrid[int(y)][int(x)] = '#'

                    changeButton = player.buttons[y][x]
                    changeButton["bg"] = destroyedCol
                    
                msg = ("\n ==> " + player.battletag + " has sunk " + opponent.battletag + "'s " + shipObj.name + " of unit length " + str(shipObj.length))
                global turnMessages
                turnMessages.append(msg)
                
                opponent.ships.remove(shipObj)
                        
            

    def hasPlayerWon(player,opponent,aiDifficulty): #Checks if a player has won by checking if the opponent has no ships left, meaning a player has sunk them all
        if len(opponent.ships) == 0:
            global turnMessages
            
            msg = "\n\n ==> " + player.battletag + " wins in " + str(player.numOfTurns) + " turns!"
            turnMessages.append(msg)
            
            saveGameOutcome(player,opponent,aiDifficulty)

            for y in range(0,width):
                for x in range(0,width):
                    buttonColCheck = opponent.buttons[x][y]
                    if player.shipGrid[x][y] != "~" and buttonColCheck["bg"] == buttonCol:
                        buttonColCheck["bg"] = 'pink'

            return True
                    
        else:
            return False



    #Coordinate guessing

    def humanGuessColumn(width): #ASCII version of inputting coordinates to guess (used for debugging purposes)
        isAlphaChar = False
        isInRange = False
        while not(isAlphaChar and isInRange):
            isAlphaChar = False
            isInRange = False
            columnGuessed = str(input("Guess a vertical column (letter): "))
            if len(columnGuessed) == 1 and columnGuessed.isalpha():
                isAlphaChar = True
                numericColumn = letterToNum(columnGuessed)
                if int(numericColumn) > 0 and int(numericColumn) < (width+1):
                    isInRange = True

            print(isAlphaChar)
            print(isInRange)
                
        columnGuessed = numericColumn-1
        return columnGuessed

    def humanGuessRow(width): #ASCII version of inputting coordinates to guess (used for debugging purposes) like the function above
        rowGuessed = input("Guess a horizontal row (number): ")
        while len(rowGuessed) == 0 or not(rowGuessed.isnumeric()) or int(rowGuessed) < 1 or int(rowGuessed) > (width+1):
            rowGuessed = input("Guess a horizontal row (number): ")
        rowGuessed = int(rowGuessed) - 1
        return rowGuessed

    def aiRandomColumn(width): #Generates a random number to be used as a coordinate to guess at
        columnGuessed = random.randint(0,width-1)
        return columnGuessed

    def aiRandomRow(width): #Generates a random number to be used as a coordinate to guess at
        rowGuessed = random.randint(0,width-1)
        return rowGuessed



    def aiGenerateGridWithShips(currentPlayer,opponent,width): #Generates a grid with the other procedure, creates an array of ships, then places them onto the grid in random positions
        grid = generateGrid(width)
        temporaryShips = createShips()
        remainingShipNames = []
        remainingShips = []

        for shipObj in opponent.ships:
            remainingShipNames.append(shipObj.name)
     
        for shipObj in temporaryShips:
            for shipName in remainingShipNames:
                if shipObj.name == shipName:
                    remainingShips.append(shipObj)
        for shipObj in remainingShips:
            success = randomShipCoords(shipObj,grid,currentPlayer)
            if success:
                shipOntoGrid(shipObj,grid)
        return grid


    def aiMostLikelyPosition(currentPlayer,opponent,width): #The probabilty density function that generates hundreds of grids with ships on and tallies up which coordinates have ships in.
        
        multiplier = 100
        for y in range (0,width):
            for x in range (0,width):
                if currentPlayer.guessingGrid[y][x] == 'X':
                    multiplier = 5

        
        numOfGrids = multiplier*len(opponent.ships)
        numOfMatches = 0
        countingGrid = [[0]*width for _ in range(width)] #Creates a 2D array of integers the same dimensions as the game board.     

        while numOfMatches < numOfGrids:
            randomGrid = aiGenerateGridWithShips(currentPlayer,opponent,width)
            gridMatch = True
            for y in range (0,width):
                for x in range (0,width):
                    if (currentPlayer.guessingGrid[y][x] == 'X' and randomGrid[y][x] == '~') or (randomGrid[y][x] != '~' and (currentPlayer.guessingGrid[y][x] == 'O' or currentPlayer.guessingGrid[y][x] == '#')):
                        gridMatch = False

            if gridMatch:
                numOfMatches += 1
                for y in range (0,width):
                    for x in range (0,width):
                        if (randomGrid[y][x] != '~' and currentPlayer.guessingGrid[y][x] == '~'):
                            countingGrid[y][x] = countingGrid[y][x] + 1


            #Output counting grid - debugging purposes
                            
    ##    for y in range (0,width):
    ##        line = ''
    ##        for x in range (0,width):
    ##            line = (line + str(countingGrid[y][x]) + ", ")
    ##        print(line)

        #Select max value x and y coords

        maxValues = []
        
        for line in countingGrid:
            lineHighest = max(line)
            maxValues.append(lineHighest)
        highestValue = max(maxValues)
        for y in range (0,width):
            for x in range (0,width):
                if countingGrid[y][x] == highestValue:
                    coordGuess = []
                    coordGuess.append(y)
                    coordGuess.append(x)
                    return coordGuess


    #Saving game results

    def saveGameOutcome(winner,loser,aiDifficulty): #Saves the outcome of the regular battleships game
        outcomesFile = open("gameOutcomesRegular.csv","a")
        outcomesFile.write("\n" + winner.username + "," + loser.username + "," + str(aiDifficulty) + "," + str(winner.numOfTurns) + "," + str(loser.numOfTurns))
        outcomesFile.close() 

    #Grid generations:

    width = 10

    player1ShipGrid = generateGrid(width)
    player2ShipGrid = generateGrid(width)

    player1Ships = createShips()
    player2Ships = createShips()

    global player1
    global player2

    player1Buttons = []
    player2Buttons = []
    
    player1 = player(username,battletag,True,player1Ships,player1ShipGrid,generateGrid(width),player1Buttons)
    if onePlayer:
        player2 = player("Computer","AI",False,player2Ships,player2ShipGrid,generateGrid(width),player2Buttons)
    else:
        player2 = player("Guest","Guest player 2",True,player2Ships,player2ShipGrid,generateGrid(width),player2Buttons)

    #1 is random guesses, 2 is probability guessing
    global aiDifficulty
    aiDifficulty = 2

    if not(player1.humanPlayer) and not(player2.humanPlayer):
        aiDifficulty = 0

    for shipObj in player1.ships:
        setCoords = randomShipCoords(shipObj,player1.shipGrid,player2)
        shipOntoGrid(shipObj,player1.shipGrid)
        
    for shipObj in player2.ships:
        setCoords = randomShipCoords(shipObj,player2.shipGrid,player1)
        shipOntoGrid(shipObj,player2.shipGrid)

    global font1
    global font2
    font1 = ("Courier",13)
    font2 = ("Courier",24)

    global missCol
    missCol = col4
    global hitCol
    hitCol = col0
    global destroyedCol
    destroyedCol = col3
    global buttonCol
    buttonCol = col2
    global backgroundCol
    backgroundCol = col1

    global screen
    screen = Tk()
    screen.configure(bg = backgroundCol)

    frameLeft = LabelFrame(screen,bg = backgroundCol,borderwidth=0,highlightthickness=0)
    frameMid = LabelFrame(screen,bg = backgroundCol,borderwidth=0,highlightthickness=0)
    frameRight = LabelFrame(screen,bg = backgroundCol,borderwidth=0,highlightthickness=0)

    def insertIntoMessageLog(textBox,msg): #Inserts a string into the scrolled text tkinter widget.
        textArea.configure(state ='normal')
        textBox.insert(END, msg)
        textArea.configure(state ='disabled')

    global p1TurnText
    global p1NotTurnText
    global p2TurnText
    global p2NotTurnText
    p1TurnText = "★PLAYER 1★"
    p1NotTurnText = "☆PLAYER 1☆"
    p2TurnText = "★PLAYER 2★"
    p2NotTurnText = "☆PLAYER 2☆"


    global p1TextLabels
    p1TextLabels = []
    global p2TextLabels
    p2TextLabels = []

    #Displays the text that will be shown above the grids in the gameplay
    for char in range(0,len(p1TurnText)):
        label = Label(frameLeft,text=p1TurnText[char],fg=buttonCol,bg=backgroundCol,font = font2)
        label.grid(row=0,column=char)
        p1TextLabels.append(label)

    for char in range(0,len(p2NotTurnText)):
        label = Label(frameRight,text=p2NotTurnText[char],fg=buttonCol,bg=backgroundCol,font = font2)
        label.grid(row=0,column=char)
        p2TextLabels.append(label)

    #Creating a scrolled text widget for the Event log
    global textArea
    textArea = st.ScrolledText(frameMid,font = font1,fg=buttonCol, bg = backgroundCol,width = 34,height = 24,wrap=WORD)
    textArea.insert(END, " ====> THINK AND SINK\n")
    textArea.insert(END, " ==> Regular Battleships vs AI\n")


    textArea.insert(END, "\n ==> Player 1 - " + player1.battletag + "\n")
    textArea.insert(END, " ==> Player 2 - " + player2.battletag + "\n")



    textArea.grid(column = 0)
    textArea.configure(state ='disabled')
        

    quitButton = Button(frameMid,font=font2,fg=backgroundCol,bg=buttonCol,width = 15,height=1,text="QUIT",padx=5,pady=5,relief=RIDGE,bd = 10, command = lambda gameScreen=screen:quitGame(gameScreen))
    quitButton.grid(row=1)

    global turnMessages
    turnMessages = []

    global currentTurn
    currentTurn = "Player 1"

    global gameInProgress
    gameInProgress = True

    def clickedGrid1(x,y): #This procedure is run when a button is clicked in player 1's guessing grid. The x and y coordinates are passed as parameters of the button that was clicked
        global gameInProgress
        if gameInProgress:
            global currentTurn
            global turnMessages
            turnMessages = []
            if currentTurn == "Player 1": #Checks if it is player 1's turn.
                if (player1.humanPlayer): #Checks if player 1 is a human player.
                    buttonGuessed = player1.buttons[y][x] #Set a variable buttonGuessed to be the button the user clicked on. 
                    if (buttonGuessed["bg"] == buttonCol): #Checks if the button guessed is its normal colour (green)
                        if player2.shipGrid[y][x] == '~': #Checks if there is no ship in this coordinate. 
                            player1.guessingGrid[y][x] = 'O' #If so, sets the guessing grid coord to be a miss 'O'.
                            buttonGuessed["bg"] = missCol #Sets the background of the button guessed to be the colour of a miss (grey)
                        else:
                            player1.guessingGrid[y][x] = 'X' #If there was aa ship in the coordinate guessed, set the coord in the guessing grid to a hit 'X'
                            player2.shipGrid[y][x] = '~' #Remove that coordinate of the ship from the opponent's ship grid. 
                            buttonGuessed["bg"] = hitCol #Set the colour of the guessed button to be the hit colour (red)

                        removeIfSunk(player1,player2) #Calls the procedure that checks if any of the ships were sunk on that turn
                        player1.numOfTurns += 1 #Increments the turn count for player 1.
                        if (hasPlayerWon(player1,player2,aiDifficulty)):
                            gameInProgress = False
                        currentTurn = "Player 2" #Switches the turn over to player 2.
                        
                        #Player 1 turn switches over to player 2
                        for index in range(0,len(p1TextLabels)):
                            label = p1TextLabels[index]
                            label["text"] = p1NotTurnText[index]
                        for index in range(0,len(p2TextLabels)):
                            label = p2TextLabels[index]
                            label["text"] = p2TurnText[index]


            if currentTurn == "Player 2": #Checks if it is player 2's turn.
                if not(player2.humanPlayer): #Checks if player 2 is an AI player (not human)
                    loop = True #Sets a boolean variable to True that will be used to loop until a coord is chosen not previously guessed
                    while loop: #Iterates the code below until the loop variable is set to false
                        if aiDifficulty == 1: #Checks if the difficulty of the AI is level 1
                            rndX = aiRandomColumn(len(player2.guessingGrid)) #If so, calls the functions responsible for making the guesses
                            rndY = aiRandomRow(len(player2.guessingGrid))
                        elif aiDifficulty == 2: #Checks if the difficulty of the AI is level 2
                            mostLikelyCoord = aiMostLikelyPosition(player2,player1,len(player2.guessingGrid)) #If so, calls the function responsible for maaking the coord guess
                            rndY = int(mostLikelyCoord[1]) #Sets the x and y guessing variables to be the corresponding return values from the list from the function called above.
                            rndX = int(mostLikelyCoord[0])
                        buttonGuessed = player2.buttons[rndX][rndY] #Sets a variable called button guessed to the matching button widget from the player 2 buttons 2D array
                        if (buttonGuessed["bg"] == buttonCol): #Checks if the colourt of the button is normal and unchanged (meaning it has not been guessed yet)
                            if player1.shipGrid[rndX][rndY] == '~': #Checks if there is no ship in the coordinate guessed. 
                                player2.guessingGrid[rndX][rndY] = 'O' #If so, sets the coordinate to be a miss on the guessing grid 'O'
                                buttonGuessed["bg"] = missCol #Sets the colour of the button widget to be the colour of a miss (grey)
                            else:
                                player2.guessingGrid[rndX][rndY] = 'X' #Sets the coord guesses to be aa hit 'X'
                                player1.shipGrid[rndX][rndY] = '~' #Removes the ship's symbol from the opponent's ship grid
                                buttonGuessed["bg"] = hitCol #Sets the colour of the button widget guessed to be the colour matching a hit (red)

                            player2.numOfTurns += 1 #Increments the player's turn count
                            currentTurn = "Player 1" #Switchs the turn back over top player 1.
                            removeIfSunk(player2,player1) #Calls the procedure responsible for checking if any ships have been sunk on that turn
                            if (hasPlayerWon(player2,player1,aiDifficulty)):
                                gameInProgress = False

                            #Player 2 turn switches over to player 1
                            for index in range(0,len(p1TextLabels)):
                                label = p1TextLabels[index]
                                label["text"] = p1TurnText[index]
                            for index in range(0,len(p2TextLabels)):
                                label = p2TextLabels[index]
                                label["text"] = p2NotTurnText[index]

                            loop = False #Ends the while loop by setting the temporary loop variable to false
                            
                addedMessage = ""
                for message in turnMessages:
                    addedMessage = addedMessage + message
                for time in range(0,len(addedMessage)):
                    screen.after(time*10,lambda textBox=textArea,msg=addedMessage[time]:insertIntoMessageLog(textBox,msg))

        if currentTurn == "Player 1" and not(player1.humanPlayer and player2.humanPlayer):
            clickedGrid2(1,1)

    def clickedGrid2(x,y): #This procedure is run when a button is clicked in player 2's guessing grid. The x and y coordinates are passed as parameters of the button that was clicked
        global gameInProgress
        if gameInProgress:
            global currentTurn
            global turnMessages
            turnMessages = []
            if currentTurn == "Player 2": #Checks if it is player 2's turn.
                if (player2.humanPlayer): #Checks if player 2 is a human player.
                    buttonGuessed = player2.buttons[y][x] #Set a variable buttonGuessed to be the button the user clicked on. 
                    if (buttonGuessed["bg"] == buttonCol): #Checks if the button guessed is its normal colour (green)
                        if player1.shipGrid[y][x] == '~': #Checks if there is no ship in this coordinate. 
                            player2.guessingGrid[y][x] = 'O' #If so, sets the guessing grid coord to be a miss 'O'.
                            buttonGuessed["bg"] = missCol #Sets the background of the button guessed to be the colour of a miss (grey)
                        else:
                            player2.guessingGrid[y][x] = 'X' #If there was a ship in the coordinate guessed, set the coord in the guessing grid to a hit 'X'
                            player1.shipGrid[y][x] = '~' #Remove that coordinate of the ship from the opponent's ship grid. 
                            buttonGuessed["bg"] = hitCol #Set the colour of the guessed button to be the hit colour (red)

                        removeIfSunk(player2,player1) #Calls the procedure that checks if any of the ships were sunk on that turn
                        player2.numOfTurns += 1 #Increments the turn count for player 2.
                        if (hasPlayerWon(player2,player1,aiDifficulty)):
                            gameInProgress = False
                            
                        currentTurn = "Player 1" #Switches the turn over to player 1.

                        #Player 2 turn switches over to player 1
                        for index in range(0,len(p1TextLabels)):
                            label = p1TextLabels[index]
                            label["text"] = p1TurnText[index]
                        for index in range(0,len(p2TextLabels)):
                            label = p2TextLabels[index]
                            label["text"] = p2NotTurnText[index]


            if currentTurn == "Player 1": #Checks if it is player 1's turn.
                if not(player1.humanPlayer): #Checks if player 1 is an AI player (not human)
                    loop = True #Sets a boolean variable to True that will be used to loop until a coord is chosen not previously guessed
                    while loop: #Iterates the code below until the loop variable is set to false
                        if aiDifficulty == 1: #Checks if the difficulty of the AI is level 1
                            rndX = aiRandomColumn(len(player1.guessingGrid)) #If so, calls the functions responsible for making the guesses
                            rndY = aiRandomRow(len(player1.guessingGrid))
                        elif aiDifficulty == 2: #Checks if the difficulty of the AI is level 2
                            mostLikelyCoord = aiMostLikelyPosition(player1,player2,len(player1.guessingGrid)) #If so, calls the function responsible for maaking the coord guess
                            rndY = int(mostLikelyCoord[1]) #Sets the x and y guessing variables to be the corresponding return values from the list from the function called above.
                            rndX = int(mostLikelyCoord[0])
                        buttonGuessed = player1.buttons[rndX][rndY] #Sets a variable called button guessed to the matching button widget from the player 2 buttons 2D array
                        if (buttonGuessed["bg"] == buttonCol): #Checks if the colourt of the button is normal and unchanged (meaning it has not been guessed yet)
                            if player2.shipGrid[rndX][rndY] == '~': #Checks if there is no ship in the coordinate guessed. 
                                player1.guessingGrid[rndX][rndY] = 'O' #If so, sets the coordinate to be a miss on the guessing grid 'O'
                                buttonGuessed["bg"] = missCol #Sets the colour of the button widget to be the colour of a miss (grey)
                            else:
                                player1.guessingGrid[rndX][rndY] = 'X' #Sets the coord guesses to be aa hit 'X'
                                player2.shipGrid[rndX][rndY] = '~' #Removes the ship's symbol from the opponent's ship grid
                                buttonGuessed["bg"] = hitCol #Sets the colour of the button widget guessed to be the colour matching a hit (red)

                            player1.numOfTurns += 1 #Increments the player's turn count
                            currentTurn = "Player 2" #Switchs the turn back over to player 2.
                            removeIfSunk(player1,player2) #Calls the procedure responsible for checking if any ships have been sunk on that turn
                            if (hasPlayerWon(player1,player2,aiDifficulty)):
                                gameInProgress = False

                            #Player 1 turn switches over to player 2
                            for index in range(0,len(p1TextLabels)):
                                label = p1TextLabels[index]
                                label["text"] = p1NotTurnText[index]
                            for index in range(0,len(p2TextLabels)):
                                label = p2TextLabels[index]
                                label["text"] = p2TurnText[index]
        
                            loop = False #Ends the while loop by setting the temporary loop variable to false
                            
                addedMessage = ""
                for message in turnMessages:
                    addedMessage = addedMessage + message
                for time in range(0,len(addedMessage)):
                    screen.after(time*2,lambda textBox=textArea,msg=addedMessage[time]:insertIntoMessageLog(textBox,msg))

        if currentTurn == "Player 2" and not(player1.humanPlayer and player2.humanPlayer):
            clickedGrid1(1,1)

    for y in range(0,len(player1.guessingGrid)):
        line = []
        for x in range(0,len(player1.guessingGrid)):
            b = Button(frameLeft, bd=4, relief=RIDGE, width=4, height=2,fg=backgroundCol,bg=buttonCol,command=lambda x=x,y=y:clickedGrid1(x,y),activebackground="blue")
            b.grid(row=y+1,column=x)
            line.append(b)
        player1.buttons.append(line)

    for y in range(0,len(player2.guessingGrid)):
        line = []
        for x in range(0,len(player2.guessingGrid)):
            b = Button(frameRight, bd=4, relief=RIDGE, width=4, height=2,fg=backgroundCol,bg=buttonCol,command=lambda x=x,y=y:clickedGrid2(x,y),activebackground="blue")
            b.grid(row=y+1,column=x)
            line.append(b)
        player2.buttons.append(line)

    frameLeft.grid(row = 0,column = 0)
    frameMid.grid(row = 0,column = 1)
    frameRight.grid(row = 0,column = 2)

    screen.mainloop()

###########################################################################################

























#Below is the code for the game mode CHAOS MODE - a single player version of hunting down moving ships with interesting attacks and abilities

def gameChaosMode(username,battletag):


    if musicOn.get() == 1:
        winsound.PlaySound('chaosMode.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
    else:
        winsound.PlaySound(None,winsound.SND_ASYNC)

    #A class for the player in the chaos mode version of the game
    class playerChaosMode:
        numOfTurns = 0
        username = ''
        battletag = ''
        time = 0
        shipGrid = [[]]

        def __init__(self,setUsername,setBattletag,setShipGrid): #Initialiser method for the player object creation
            self.username = setUsername
            self.battletag = setBattletag
            self.shipGrid = setShipGrid
            
    #A class for the ships in chaos mode
    class ship:
        name = ''
        length = 0
        symbol = ''
        h_direction = 0 #1 right, -1 left
        v_direction = 0 #1 down, -1 up
        frontX = int(0)
        frontY = int(0)
        xCoords = []
        yCoords = []
        hitpoints = 0
        maxHitpoints = 0

        def __init__(self,setName,setSymbol,setLength,setHDirection,setVDirection,setFrontX,setFrontY,setXcoords,setYcoords,setHitpoints): #Initialiser method for the ship object creation
            self.name = setName
            self.symbol = setSymbol
            self.length = setLength
            self.h_direction = setHDirection
            self.v_direction = setVDirection
            self.frontX = setFrontX
            self.frontY = setFrontY
            self.xCoords = setXcoords
            self.yCoords = setYcoords
            self.hitpoints = setHitpoints
            self.maxHitpoints = setHitpoints

    #A class for the different attacks available in chaos mode
    class attack:
        name = ''
        damage = 0
        cooldown = 0
        
        def __init__(self,setName,setDamage,setButton,setCooldown): #Initialiser method for the attack objects' creation
            self.name = setName
            self.damage = setDamage
            self.button = setButton
            self.cooldown = setCooldown

        def changeButtonCol(self, colour):
            self.button["bg"] = colour



    #Gameplay procedures

    def generateGrid(width): #Same as in regular mode, generates a blnk grid.
        grid = [["~"]*width for _ in range(width)]
        return grid

    def randomHdirection(): #Same as in regular game mode
        horizOrVert = random.randint(1,2) #1 for horizontal, 2 for vertical
        h_direction = 0
        if horizOrVert == 1:
            while h_direction == 0:
                h_direction = random.randint(-1,1)
        return h_direction

    def randomVdirection(h_direction): #Same as in regular game mode
        v_direction = random.randint(-1,1)
        if h_direction == 0:
            while v_direction == 0:
                v_direction = random.randint(-1,1)
        else:
            v_direction = 0
        return v_direction

    def createShips(): #Same as in regular game mode, except for the creation of an additional 2 ships of longer length
        
        #setName,setSymbol,setLength,setHDirection,setVDirection,setX,setY,setXcoords,setYcoords,setHitpoints

        longship = ship("Longship", "L",7,0,0,0,0,[],[],1000)
        carrier = ship("Aircraft carrier", "A",5,0,0,0,0,[],[],750)
        battleship = ship("Battleship", "B",4,0,0,0,0,[],[],750)
        galleon = ship("Galleon", "G",4,0,0,0,0,[],[],750)
        submarine = ship("Submarine", "S",3,0,0,0,0,[],[],500)
        cruiser = ship("Cruiser", "C",3,0,0,0,0,[],[],500)
        destroyer = ship("Destroyer", "D",2,0,0,0,0,[],[],400)
        
        

        ships = [longship, carrier, battleship, galleon, submarine, cruiser, destroyer]
        return ships

    def createAttacks(): #Creates the attack objects that will be used to deal damage to the ships

        def changeAttack(attackName):
            global attackSelected
            for attackObj in attacks:
                if attackObj.name == attackName and attackObj.cooldown == 0:
                    attackSelected = attackName
                    attackObj.button["text"] = "--> " + attackSelected
                else:
                    attackObj.button["text"] = attackObj.name

        def hover(attackObj): #This procedure is run when a button is hovered over
            if attackObj.cooldown == 0:
                attackObj.changeButtonCol("lime")
            elif attackObj.cooldown == 1:
                attackObj.changeButtonCol("orange")
            else:
                attackObj.changeButtonCol("brown1")
        def leave(attackObj): #This procedure is run when a button is left after being hovered over
            attackObj.changeButtonCol(buttonCol)
        def click(self): #This procedure is run when a button is clicked on
            resetGridCol(buttonCol)

        attackNames = ["Torpedo","Missile","Focus laser","Bombing run horizontal","Bombing run vertical","Scattershots","Freeze","Sonar"]
        buttons = []

        for name in attackNames:
            btn = Button(frameMid, bd=3, relief=RIDGE, width=23, height=2,fg=backgroundCol,bg=buttonCol,text=name, command = lambda attackName=name:changeAttack(attackName))
            buttons.append(btn)
            
        torpedo = attack("Torpedo", 90, buttons[0], 0)
        missile = attack("Missile", 40, buttons[1], 0)
        focusLaser = attack("Focus laser", 150, buttons[2], 0)
        bombingRunH = attack("Bombing run horizontal", 70, buttons[3], 0)
        bombingRunV = attack("Bombing run vertical", 70, buttons[4], 0)
        scattershots = attack("Scattershots", 80, buttons[5], 0)
        freeze = attack("Freeze", 0, buttons[6], 0)
        sonar = attack("Sonar", 0, buttons[7], 0)

        attacks = [torpedo, missile, focusLaser, bombingRunH, bombingRunV, scattershots, freeze, sonar]

        for attackObj in attacks:
            btn = attackObj.button
            btn.bind('<Enter>', lambda event, attackObj=attackObj: hover(attackObj))
            btn.bind('<Leave>', lambda event, attackObj=attackObj: leave(attackObj))
            btn.bind('<Button-1>', click)


        return attacks


    def randomShipCoords(ship,grid): #Generates random coordinates for a ship on a grid passed as parameters
        positionAvailable = False
        while positionAvailable == False:

            positionAvailable = True
                
            ship.xCoords = []
            ship.yCoords = []

            horizontalDirection = randomHdirection()
            verticalDirection = randomVdirection(horizontalDirection)
            ship.h_direction = horizontalDirection
            ship.v_direction = verticalDirection

            rnd1 = random.randint(0,len(grid)-1)
            rnd2 = random.randint(0,len(grid)-1)
            ship.frontX = rnd1
            ship.frontY = rnd2
            
            XandYcoords(ship)

            for n in range (0,ship.length):
                x = int(ship.xCoords[n])
                y = int(ship.yCoords[n])
                gridWidth = len(grid) - 1
                if not(x > gridWidth or x < 0 or y > gridWidth or y < 0):
                    if grid[y][x] != "~":
                        positionAvailable = False
                else:
                    positionAvailable = False
        return True

    def XandYcoords(ship): #Same as regular mode
        Xmultiplier = -(ship.h_direction)
        Ymultiplier = -(ship.v_direction)
        ship.xCoords = []
        ship.yCoords = []
        for i in range (0,ship.length):
            ship.yCoords.append(str(int(ship.frontY)+(i*Ymultiplier)))
        for j in range (0,ship.length):
            ship.xCoords.append(str(int(ship.frontX)+(j*Xmultiplier)))

    def shipOntoGrid(ship,player): #Same as in regular mode, places a ship onto a grid
        for n in range (0,ship.length):
            x = int(ship.xCoords[n])
            y = int(ship.yCoords[n])
            player.shipGrid[y][x] = ship.symbol


    def removeIfSunk(player,ships,grid): #Loops through all of a players' remaining ships and checks for any to remove from the array if they are sunk.
        for shipObj in ships:
            if shipObj.hitpoints <= 0:  
                msg = ("\n====> " + player.battletag + " has sunk " + shipObj.name + " of unit length " + str(shipObj.length))
                global turnMessages
                turnMessages.append(msg)
                for y in range(0,len(grid)):
                    for x in range(0,len(grid)):
                        if grid[y][x] == shipObj.symbol:
                            grid[y][x] = "~"

                shipObj.correspondingButton.destroy()
                
                global sunkenShips
                sunkenShips += 1

                shipSunkButton = Button(frameMid2, bd=3, relief=RIDGE, width=29, height=2,fg=backgroundCol,bg=sunkCol,text=shipObj.name + ": SUNK",activebackground="purple")
                shipSunkButton.grid(row=10+sunkenShips)
                
                ships.remove(shipObj)


    def moveShip(shipToMove,ships): #Moves a ship one cell in the direction it is facing - if it is touching the edge of the board or another ship, it will rotate 180 degrees, so its front coordinate will become its rear coordinate and vice versa
        
        canMove = True
        newX = int(shipToMove.frontX) + int(shipToMove.h_direction)
        newY = int(shipToMove.frontY) + int(shipToMove.v_direction)
        
        for shipToCheck in ships:
            if shipToMove.name != shipToCheck.name:
                for n in range(0,shipToCheck.length):
                    if (newX < 0 or newX > (width-1) or newY < 0 or newY > (width-1)):
                        canMove = False
                    elif (int(newX) == int(shipToCheck.xCoords[n]) and int(newY) == int(shipToCheck.yCoords[n])):
                        canMove = False
            if len(ships) == 1:
                for n in range(0,shipToCheck.length):
                    if (newX < 0 or newX > (width-1) or newY < 0 or newY > (width-1)):
                        canMove = False
                    
                
        if canMove:
            shipToMove.frontX = newX
            shipToMove.frontY = newY
            XandYcoords(shipToMove)
        else:
            shipToMove.frontX = shipToMove.xCoords[shipToMove.length-1]
            shipToMove.frontY = shipToMove.yCoords[shipToMove.length-1]
            shipToMove.h_direction = -(shipToMove.h_direction)
            shipToMove.v_direction = -(shipToMove.v_direction)
            XandYcoords(shipToMove)
            
    def hasGameEnded(player,ships): #Checks if the player has sunk all the ship and thus if the game has ended
        if len(ships) == 0:
            global turnMessages
            global startingTime
            
            endingTime = datetime.now()
            timeDifference = format(endingTime - startingTime)
            timeString = str(timeDifference)
            
            seconds = float(timeString[5:])
            minutes = int(timeString[2:4])
            hours = int(timeString[0])


            totalSeconds = (hours*3600) + (minutes*60) + (seconds)
            
            player.time = round(totalSeconds)
            
            msg = "\n\n ==> " + player.battletag + " wins in " + str(player.numOfTurns) + " turns with a time of " + str(player.time) + " seconds!"
            turnMessages.append(msg)

            
            
            saveGameOutcome(player)            
            return True
        else:
            return False

    def saveGameOutcome(player): #Saves the game outcome to a csv file and the online database. 
        outcomesFile = open("gameOutcomesChaos.csv","a")
        outcomesFile.write("\n" + player.username + "," + player.battletag + "," + str(player.numOfTurns) + "," + str(player.time))
        outcomesFile.close()

        # DB OBJECT
        mydb = mysql.connector.connect(
          host="userwebs.hallcross.org",
          user="wals7255",
          password="WxJM4z",
          database="wals7255"
        )
        mycursor = mydb.cursor()
         
        # INSERT RECORDS
        sql_insert = "INSERT INTO gameOutcomes (username, battletag, turns, time) VALUES ('{}', '{}', '{}', '{}')".format(player.username, player.battletag, str(player.numOfTurns), str(player.time))
        mycursor.execute(sql_insert)
        mydb.commit()
        

    #Defining variables

    global width
    width = 12
    playerShipGrid = generateGrid(width)
    global gridButtons
    gridButtons = []
    player = playerChaosMode(username,battletag,playerShipGrid)
    global gameInProgress
    gameInProgress = True

    global ships
    ships = createShips()

    for shipObj in ships:
        setCoords = randomShipCoords(shipObj,player.shipGrid)
        shipOntoGrid(shipObj,player)

    global missCol
    missCol = col4
    global hitCol
    hitCol = col0
    global buttonCol
    buttonCol = col2
    global backgroundCol
    backgroundCol = col1
    global sunkCol
    sunkCol = col3
    global hoverCol
    hoverCol = col5
        

    global screen
    screen = Tk()
    screen.configure(bg = backgroundCol)

    global font1
    global font2
    font1 = ("Courier",13)
    font2 = ("Courier",24)

    global frameLeft
    global frameMid
    global frameMid2
    global frameRight
    frameLeft = LabelFrame(screen,bg = backgroundCol,borderwidth=10,highlightthickness=0)
    frameMid = LabelFrame(screen,bg = backgroundCol,borderwidth=10,highlightthickness=0)
    frameMid2 = LabelFrame(screen,bg = backgroundCol,borderwidth=10,highlightthickness=0)
    frameRight = LabelFrame(screen,bg = backgroundCol,borderwidth=10,highlightthickness=0)


    global sunkenShips
    sunkenShips = 0

    global textArea
    textArea = st.ScrolledText(frameRight,font = font1,fg=buttonCol, bg = backgroundCol,width = 30,height = 26,wrap=WORD)
    textArea.insert(END, " ====> THINK AND SINK\n")
    textArea.insert(END, " ==> Chaos Mode - one player\n")

    textArea.insert(END, "\n ==> Player - " + player.battletag + "\n")
    textArea.grid(row=0)
    textArea.configure(state ='disabled')

    global gridFrozen
    gridFrozen = False

    global turnMessages
    turnMessages = []

    global attackSelected
    attackSelected = ""

    global startingTime
    startingTime = datetime.now()

    def numToLetter(num): #Converts a number to a letter 
        num2alpha = dict(zip(range(1, 27), string.ascii_uppercase))
        letter = num2alpha[num]
        return letter

    def letterToNum(letter): #Converts a letter to a number
        letter = letter.upper()
        alpha2num = dict(zip(string.ascii_uppercase, range(1, 27)))
        num = alpha2num[letter]
        return num

    def displayGrid(grid): #Outputs the grid to the python shell display in a text based format (debugging purposes)
        line = ""
        num = (len(grid)*2)+3
        outline = "   "
        topnumbers = "     "
        for x in range (1,len(grid)+1):
            col = numToLetter(x)
            topnumbers = topnumbers + col + " "
        print(topnumbers)
        for i in range(0,num):
            outline = outline + "-"
        print(outline)
        for y in range (0,len(grid)):
            for x in range (0,len(grid)):
                line = line + " " + grid[y][x]
            if len(str(y+1)) == 1:
                print(str(y+1) + "  ¦" + line + " ¦")
            else:
                print(str(y+1) + " ¦" + line + " ¦")
            line = ""
        print(outline)


    def MoveAllShips(player,ships): #This loops through all the ships and moves all of them consecutively
        player.shipGrid = generateGrid(width)
        for shipObj in ships:
            moveShip(shipObj,ships)
        for shipObj in ships:
            shipOntoGrid(shipObj,player)
                

    def resetGridCol(col): #Resets the colour of all the backgrounds of all the buttons on the game grid for chaos mode
        for yCoord in range(0,len(gridButtons)):
            for xCoord in range(0,len(gridButtons)):
                changeButtonCol = gridButtons[yCoord][xCoord]
                changeButtonCol["bg"] = col

    def insertIntoMessageLog(textBox,msg): #Inserts a string passed as a parameter into a scrolled text tkinter widget
        textArea.configure(state ='normal')
        textBox.insert(END, msg)
        textArea.configure(state ='disabled')




    for x in range(width):
        char = numToLetter(x+1)
        lbl = Label(frameLeft, bd=4, width=4, height=2,fg=buttonCol,bg=backgroundCol, text=char)
        lbl.grid(row=0,column=x+1)

    for y in range(width):
        lbl = Label(frameLeft, bd=4, width=4, height=2,fg=buttonCol,bg=backgroundCol, text=str(y+1))
        lbl.grid(row=y+1,column=0)





        
        
        
    for y in range(0,len(player.shipGrid)):
        line = []
        for x in range(0,len(player.shipGrid)):

            def make3x3Square(x,y): #Makes a 3x3 square around where was clicked and add the buttons in this area into an array called targets
                targets = []
                for i in range(x-1,x+2):
                    for j in range(y-1,y+2):
                        if (i <= (width-1) and j <= (width-1)) and (i >= 0 and j >= 0):
                            b = gridButtons[j][i]
                            targets.append(b)
                return targets

            def makeCircle(x,y): #Makes a circle around where was clicked and add the buttons in this area into an array called targets
                targets = []
                for i in range(x-2,x+3):
                    for j in range(y-2,y+3):
                        if i <= (width-1) and j <= (width-1) and (i >= 0 and j >= 0):
                            b = gridButtons[j][i]
                            targets.append(b)
                for i in range(x-1,x+2):
                    for j in range(y-3,y+4):
                        if i <= (width-1) and j <= (width-1) and (i >= 0 and j >= 0):
                            b = gridButtons[j][i]
                            targets.append(b)

                for i in range(x-3,x+4):
                    for j in range(y-1,y+2):
                        if i <= (width-1) and j <= (width-1) and (i >= 0 and j >= 0):
                            b = gridButtons[j][i]
                            targets.append(b)
                    
                return targets

            def make3x3Cross(x,y): #Makes a 3x3 cross around where was clicked and add the buttons in this area into an array called targets
                targets = []
                for i in range(x-1,x+2):
                    if i <= (width-1) and i >= 0:
                        b = gridButtons[y][i]
                        targets.append(b)
                for j in range(y-1,y+2):
                    if j <= (width-1) and j >= 0:
                        b = gridButtons[j][x]
                        targets.append(b)
                return targets

            def makeHorizontalLine(x,y): #Makes a row where was clicked and adds the buttons in this area into an array called targets
                targets = []
                for j in range(0,width):
                    b = gridButtons[j][x]
                    targets.append(b)
                return targets

            def makeVerticalLine(x,y): #Makes a row where was clicked and adds the buttons in this area into an array called targets
                targets = []
                for i in range(0,width):
                    b = gridButtons[y][i]
                    targets.append(b)
                return targets

            

            def on_leave(x,y): #This is called when the mouse cursor leaves the region of a button
                targets = []
                global attackSelected
                global attackArray

                if attackSelected == "Torpedo":
                    targets = make3x3Square(x,y)
                elif attackSelected == "Missile":
                    targets = makeCircle(x,y)
                elif attackSelected == "Focus laser":
                    targets = make3x3Cross(x,y)
                elif attackSelected == "Bombing run horizontal":
                    targets = makeHorizontalLine(x,y)
                elif attackSelected == "Bombing run vertical":
                    targets = makeVerticalLine(x,y)
                elif attackSelected == "Scattershots":
                    singleButton = gridButtons[y][x]
                    targets = [singleButton]

                for target in targets:
                    if target['bg'] == 'pink':
                        target['bg'] = buttonCol


            def on_enter(x,y): #This is called when the mouse cursor enters the region of a button
                targets = []
                global attackSelected
                global attackArray

                if attackSelected == "Torpedo":
                    targets = make3x3Square(x,y)
                elif attackSelected == "Missile":
                    targets = makeCircle(x,y)
                elif attackSelected == "Focus laser":
                    targets = make3x3Cross(x,y)
                elif attackSelected == "Bombing run horizontal":
                    targets = makeHorizontalLine(x,y)
                elif attackSelected == "Bombing run vertical":
                    targets = makeVerticalLine(x,y)
                elif attackSelected == "Scattershots":
                    singleButton = gridButtons[y][x]
                    targets = [singleButton]

                for target in targets:
                    if target['bg'] == buttonCol:
                        target['bg'] = 'pink'

            def on_click(x,y): #This is called when the mouse clicks a button
                targets = []
                global attackSelected
                global attackArray

                def numOfScattershots(): #Returns the number of scattershot selected, as the maximum that should be checked for is 10
                    count = 0
                    for yCoord in range(0,len(gridButtons)):
                        for xCoord in range(0,len(gridButtons)):
                            checkBtnCol = gridButtons[yCoord][xCoord]
                            if checkBtnCol["bg"] == hitCol:
                                count += 1
                    return count

                if attackSelected == "Torpedo":
                    resetGridCol(buttonCol)
                    targets = make3x3Square(x,y)
                elif attackSelected == "Missile":
                    resetGridCol(buttonCol)
                    targets = makeCircle(x,y)
                elif attackSelected == "Focus laser":
                    resetGridCol(buttonCol)
                    targets = make3x3Cross(x,y)
                elif attackSelected == "Bombing run horizontal":
                    resetGridCol(buttonCol)
                    targets = makeHorizontalLine(x,y)
                elif attackSelected == "Bombing run vertical":
                    resetGridCol(buttonCol)
                    targets = makeVerticalLine(x,y)
                elif attackSelected == "Scattershots":
                    if (numOfScattershots() < 10):
                        singleButton = gridButtons[y][x]
                        targets = [singleButton]
                elif attackSelected == "Freeze":
                    resetGridCol("cyan")
                elif attackSelected == "Sonar":
                    resetGridCol(missCol)
                    

                for target in targets:
                    target['bg'] = hitCol


            b = Button(frameLeft, bd=4, relief=RIDGE, width=4, height=2,fg=backgroundCol,bg=buttonCol,activebackground=hoverCol)
            
            b.bind('<Leave>', lambda event, x=x, y=y: on_leave(x,y))
            b.bind('<Enter>', lambda event, x=x, y=y: on_enter(x,y))
            b.bind('<Button-1>', lambda event, x=x, y=y: on_click(x,y))
            b.grid(row=x+1,column=y+1)
            line.append(b)
        gridButtons.append(line)

    rowCounter = 1
    global attackArray
    attackArray = createAttacks()

    attackTitleFont = ("Courier",24)
    label = Label(frameMid,text="ATTACKS:",bg=backgroundCol,fg=buttonCol,font = attackTitleFont)
    label.grid(row=0,column=0)

    for attackInstance in attackArray:
        button = attackInstance.button
        button.grid(row=rowCounter+1)
        rowCounter += 1
    Label(frameMid,bg=backgroundCol).grid(row=rowCounter+1)


    def confirmAttack(self): #This procedure is called when the confirm button is clicked after selecting an attack and choosing where to attack

        global gameInProgress
        if gameInProgress == True:
            global turnMessages
            
            global attackSelected
            allGreen = True

            for y in range(0,len(gridButtons)):
                for x in range(0,len(gridButtons)):
                    checkBtnCol = gridButtons[y][x]
                    if checkBtnCol["bg"] != buttonCol:
                        allGreen = False
                    
                    
            if attackSelected != "" and not(allGreen):
                player.numOfTurns += 1
                    
                xCoordsGuessed = []
                yCoordsGuessed = []
                for y in range(0,len(gridButtons)):
                    line = []
                    for x in range(0,len(gridButtons)):
                        checkBtnCol = gridButtons[y][x]
                        if checkBtnCol["bg"] == hitCol:
                            xCoordsGuessed.append(x)
                            yCoordsGuessed.append(y)
                        if attackSelected != "Sonar":
                            checkBtnCol["bg"] = buttonCol
                            checkBtnCol["text"] = ""

                numberOfHits = 0
                totalDamageDealt = 0

                if attackSelected == "Sonar":
                    for shipObj in ships:
                        btnChange = gridButtons[int(shipObj.frontY)][int(shipObj.frontX)]
                        btnChange["bg"] = hoverCol
                        btnChange["text"] = str(shipObj.length)
                        
                    sonarMessage = "\n==> " + player.battletag + " has used Sonar - the ships are revealed..."
                    turnMessages.append(sonarMessage)

                if attackSelected == "Freeze":
                    global gridFrozen
                    gridFrozen = True
                    freezeMessage = "\n==> " + player.battletag + " said Freeze! And the ocean froze..."
                    turnMessages.append(freezeMessage)

                if gridFrozen == False:
                    MoveAllShips(player,ships)

                for attackObj in attackArray:
                    if attackObj.name == attackSelected and attackObj.cooldown == 0:
                        
                        for n in range(0,len(xCoordsGuessed)):
                            xHit = xCoordsGuessed[n]
                            yHit = yCoordsGuessed[n]

                            for shipObj in ships:
                                for coordIndex in range(0,shipObj.length):
                                    xCheck = shipObj.xCoords[coordIndex]
                                    yCheck = shipObj.yCoords[coordIndex]
                                    if int(xCheck) == int(xHit) and int(yCheck) == int(yHit):
                                        shipObj.hitpoints = shipObj.hitpoints - attackObj.damage
                                        numberOfHits += 1
                                        totalDamageDealt += attackObj.damage
                        attackObj.cooldown = 3
                        attackObj.button["text"] = attackObj.name
                    if attackObj.cooldown > 0:
                        attackObj.cooldown -= 1
                    if attackObj.name == "Freeze" and attackObj.cooldown == 0:
                        gridFrozen = False

                if not(attackSelected == "Sonar" or attackSelected == "Freeze"):
                    msg1 = "\n==> " + attackSelected + " hit " + str(numberOfHits) + " ship sections"
                    turnMessages.append(msg1)
                
                removeIfSunk(player,ships,player.shipGrid)
                
                if hasGameEnded(player,ships):
                    gameInProgress = False
                    
                    
                attackSelected = ""

                addedMessage = ""
                for message in turnMessages:
                    addedMessage = addedMessage + message
                for time in range(0,len(addedMessage)):
                    screen.after(time*2,lambda textBox=textArea,msg=addedMessage[time]:insertIntoMessageLog(textBox,msg))
                turnMessages = []


                for shipObj in ships:

                    fractionOfHP = shipObj.hitpoints/shipObj.maxHitpoints
                    
                    greenValue = int(round((fractionOfHP**2)*255))
                    redValue = int(round((1-(fractionOfHP)))*255)
                    blueValue = 0

                    hexCol = b'#' + b16encode(bytes((redValue,greenValue,blueValue)))
                    
                    shipObj.correspondingButton["bg"] = hexCol
                    shipObj.correspondingButton["activebackground"] = hexCol
                    shipObj.correspondingButton["text"] = shipObj.name + ": Length " + str(shipObj.length) + "\nHitpoints " + str(shipObj.hitpoints)
                    
                


        
    confirmButton = Button(frameMid, bd=6, relief=RIDGE, width=22, height=2,fg=backgroundCol,bg=buttonCol,text="C O N F I R M")
    confirmButton.grid(row=rowCounter+2)
    confirmButton.bind('<Button-1>', confirmAttack)


    label = Label(frameMid2,text="SHIPS:",bg=backgroundCol,fg=buttonCol,font = attackTitleFont)
    label.grid(row=0,column=0)
    rowCounter = 1

    for shipObj in ships:
        shipObj.correspondingButton = Button(frameMid2, bd=3, relief=RIDGE, width=29, height=2,fg=backgroundCol,bg=buttonCol,text=shipObj.name + ": Length " + str(shipObj.length) + "\nHitpoints " + str(shipObj.hitpoints),activebackground=hoverCol)
        shipObj.correspondingButton.grid(row=rowCounter)
        rowCounter += 1

    Label(frameMid2,bg=backgroundCol,fg=buttonCol,font = attackTitleFont).grid(row=99)
    quitButton = Button(frameMid2,font=font2,fg=backgroundCol,bg=buttonCol,width = 10,height=1,text="QUIT",padx=5,pady=5,relief=RIDGE,bd = 10, command = lambda gameScreen=screen:quitGame(gameScreen))
    quitButton.grid(row=100)

    frameLeft.grid(row = 0,column = 0)
    frameMid.grid(row=0,column=1)
    frameMid2.grid(row = 0,column = 2)
    frameRight.grid(row = 0,column = 3)

    screen.mainloop()


startUp()
