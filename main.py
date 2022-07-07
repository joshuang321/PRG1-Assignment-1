import random
import os
import os.path
import math

#IMPORTANT!!!!
#make sure that there is empty folder 'highscores' and 'saves' in the same
#directory as main.py

#HOW TO USE:
#Have a python intepreter and set it to PATH enviroment variable.
#Open cmd and type 'python' to make sure you installed correctly
#Type 'python pathname' where pathname is the main.py path.
#Enjoy!

#Latest Release Simp City 2.0 Patch Notes:
#Added highscore, and save files.
#Added Custom play
#More garbage documentations

BWORD = { -1:"   ", 0:"BCH", 1:"FAC", 2:"HSE", 3:"SHP", 4:"HWY", \
          5:"PRK", 6:"MON" }
BLONGWORD = { 0: "Beach", 1:"Factory", 2:"House", 3:"Shop", 4:"Highway", \
           5:"Park", 6:"Monument" }
#New building_pool: {0:8, 1:8 ... 6:8}

#classic exit status (useless)
EXIT_SUCCESS, EXIT_FAILURE = 0, -1

#Directories used in the code
dir_path = os.path.dirname(os.path.realpath(__file__))
saves_path = dir_path + "\\saves\\"
highscore_path = dir_path + "\\highscores\\"

#Assume filename for gamefile in the form of filename.svf,
#save file extension

#Read game files using BSN, Building Short Notation.

#Format:
#dimension city;turn;buildings

#Dimension Format:
#ROW|COLUMN

#City Format:
#BCN|BCN|BCN ... |BCN

#Turn Format:
#TURN

#Building Format:
#BCN:NUM_BCN|BCN:NUM_BCN| ... |BCN:NUM_BCN


#Game Score format:
#NAME:SCORE|NAME:SCORE ... |NAME:SCORE

#city_t is just a aggregation of row, column and the board of the city
#Have to store row and column because I am using a single list
class city_t:
    def __init__(self, row, column, board = []):
        self.row, self.column, self.board =  row, column, board
        if board == []:
            self.board = [-1] * self.row * self.column

#Read gamefile
def read_gamefile(filename):
    city, turn, building_pool = None, None, None
    with open(saves_path + filename, "r") as gamefile:
        dimension, city, turn, buildings = gamefile.read().split(";")
        dimension = dimension.split("|")

        city = list(map(int, city.split("|")))
        city = city_t(int(dimension[0]), int(dimension[1]), city)
        turn = int(turn)
        buildings = buildings.split("|")

        building_pool = {}
        for index in range(len(buildings)):
            temp = buildings[index].split(":")
            building_pool[int(temp[0])] = int(temp[1])
    return city, turn, building_pool

#Saving the savefile in the saves directory
def save_gamefile(filename, city, turn, building_pool):
    with open(saves_path + filename, "w") as savefile:
        building_pool = list(building_pool.items())

        tempstr =""
        for index in range(len(building_pool)):
            tempstr = tempstr + str(building_pool[index][0]) + ":" \
                      + str(building_pool[index][1]) + "|"
        savefile.write(str(city.row) + "|" + str(city.column) + ";" \
                       + "|".join(map(str, city.board))+ ";" + str(turn) + ";" + tempstr[:-1:])
    return EXIT_SUCCESS

#Update the highscore for the top 10
def update_highscore(row, column, score):
    if not os.path.exists(highscore_path + "{}x{}.csv".format(row, column)):
        with open(highscore_path + "{}x{}.csv".format(row, column), "w") as newfile:
            pass
    
    with open(highscore_path + "{}x{}.csv".format(row, column), "r+") as scores_csv:
        scorelist = scores_csv.read()

        #Finding positions to write the new score, and
        #finding position in the leaderboard
        num_scores, position, prevfilepos = 0, 1, 0
        if scorelist == "":
            pass
        else:
            scorelist = scorelist.split("|")
            num_scores = len(scorelist)
            for scoreindex in range(num_scores):
                temp = scorelist[scoreindex].split(":")
                if int(temp[1]) <= score:
                    break
                else:
                    prevfilepos += len(scorelist[scoreindex]) + 1
                    position += 1
        #If the position is not top 10, then quit
        if position == 11:
            return EXIT_FAILURE
        print("Congratulations! You made the high score board at\n" \
                      "position {}!".format(position)) 
        name = input("Please enter your name(max 20 chars): ")

        if position == num_scores + 1 and position != 1:
            prevfilepos -= 1

        #This is to elimate the last position to make
        #space for the other players
        scores_csv.seek(prevfilepos, 0)
        tempread = scores_csv.read()
        if num_scores == 10:
            templen = len(tempread)
            for i in range(templen):
                if tempread[templen - i - 1] == "|":
                    tempread = tempread[:-i-1:]
                    break
        scores_csv.seek(prevfilepos, 0)

        #Write the name and score of the player to the file
        if position == 1:
            scores_csv.write(name + ":" + str(score))
            if num_scores != 0:
                scores_csv.write("|")
        elif position == num_scores + 1:
            scores_csv.write("|" + name + ":" + str(score))            
        else:
            scores_csv.write(name + ":" + str(score) + "|")
        scores_csv.write(tempread)
    return EXIT_SUCCESS
                

#Print highscore from a specific category
def print_highscore(filename):
    print("\n---------- HIGH SCORES ---------\n" \
                "Pos Player                 Score\n" \
                "--- ------                 -----")

    #Read the file and print the contents
    with open(highscore_path + filename, "r") as scores_csv:
        scores_csv = scores_csv.read()
        if scores_csv == "":
            pass
        else:
            scores_csv = scores_csv.split("|")
            for index in range(len(scores_csv)):
                scores_csv[index] = scores_csv[index].split(":")
                print("{:>2}. {:<20}{:>8}".format(index +1, scores_csv[index][0], \
                                                  scores_csv[index][1]))
    print("--------------------------------\n")
    return EXIT_SUCCESS

#What is the point of selecting having the same
#two buildings for options?
def random_select(building_pool, memo = []):
    #Memo stores the last building randomly selected
    #This makes it so that there is two unique building options
    building_keys = list(building_pool.keys())
    if len(building_keys) == 1:
        return building_keys[0]
    while True:
        building = random.choice(building_keys)
        if memo == []:
            building_pool[building] -= 1
            memo.append(building)
            return building
        else:
            if memo[0] == building:
                continue
            building_pool[building] -= 1
            memo.pop()
            memo.append(building)
            return building

def print_squaregrid(city):
    #UI with ascii is pain
    print("    ", end="")
    for i in range(city.column):
        print("{:^6}".format(i + 1), end = "")
    print()
    for i in range(city.row):
        print("  ", end = " ")
        for j in range(city.column):
            print("+-----", end ="")
        print("+")
        print(" " + str(i + 1), end = " ")
        for j in range(city.column):
            print("| {:^3} ".format(BWORD[city.board[i * city.column + j]]), end = "")
        print("|")
    print("  ", end = " ")
    for i in range(city.column):
        print("+-----", end ="")
    print("+")

#Print the main window of the game
def print_gui(city, turn, building_pool):
    print("Turn {}\n".format(turn))
    print_squaregrid(city)

    #Print Remaining Buildings
    print("\nBuilding           Remaining\n" \
          "--------           ---------")
    buildinglist = list(building_pool.items())
    for i in range(len(buildinglist)):
        print("{:<19}{:<9}".format(BWORD[buildinglist[i][0]], buildinglist[i][1]))

#Recursive algorithm to count parks and put
#the indexes of the parks onto a list
#The list is used to skip to reduce overcounting
def countpark(city, index, memo = []):
    memo.append(index)

    #Common theme in the code to have a checklist
    #for adjacent sides of a tile
    checklist = []
    if index%city.column != city.column - 1 and index + 1 < city.column * city.row:
        checklist.append(index + 1)

    if (index + city.column) < city.column * city.row:
        checklist.append(index + city.column)

    if index%city.column != 0 and index - 1 > -1:
        checklist.append(index - 1)

    if (index - city.column) > -1:
        checklist.append(index - city.column)

    #The checklist will be iterated and check for conditions
    for checkindex in range(len(checklist)):
        if checklist[checkindex] not in memo and city.board[checklist[checkindex]] == 5:
            countpark(city, checklist[checkindex], memo)
    return memo

#Print the scores for all the buildings
def print_score(city):
    #Buildings like factories don't need to be checked extensively for adjacent
    #conditions and thus can be simply counted
    #Monuments have cornerstones and non-cornerstones so having a single value
    scoring = { "BCH":[], "FAC":0, "HSE":[], "SHP":[], "HWY":[], "PRK":[] }
    
    hwytemp = 0
    nonconnersquares, connersquares = 0, 0
    parklist = []
    MAX_LEN = city.column * city.row
    
    #Alot of control statements...
    for index in range(MAX_LEN):
        if index%city.column == 0:
            if hwytemp != 0:
                scoring["HWY"].append(hwytemp)
            hwytemp = 0
        
        if city.board[index] == 4:
            hwytemp += 1
        else:
            if hwytemp != 0:
                scoring["HWY"].append(hwytemp)
            hwytemp = 0
            if city.board[index] == -1:
                continue
            elif city.board[index] == 0:
                if index%city.column == city.column - 1 or index%city.column == 0:
                    scoring["BCH"].append(3)
                else:
                    scoring["BCH"].append(1)
            elif city.board[index] == 1:
                scoring["FAC"] +=1
            elif city.board[index] == 2:
                checklist = []
                if index%city.column != city.column - 1 and index + 1 < MAX_LEN:
                    checklist.append(index + 1)

                if (index + city.column) < MAX_LEN:
                    checklist.append(index + city.column)

                if index%city.column != 0 and index - 1 > 0:
                    checklist.append(index - 1)

                if (index - city.column) > 0:
                    checklist.append(index - city.column)
                tempscore = []
                for checkindex in range(len(checklist)):
                    if city.board[checklist[checkindex]] == 1:
                        tempscore.clear()
                        tempscore.append(1)
                        break
                    elif city.board[checklist[checkindex]] == 2 or city.board[checklist[checkindex]] == 3:
                        tempscore.append(1)
                    elif city.board[checklist[checkindex]] == 0:
                        tempscore.append(2)

                for tempindex in range(len(tempscore)):
                    scoring["HSE"].append(tempscore[tempindex])
            elif city.board[index] == 3:
                checklist = []
                if index%city.column != city.column - 1 and index + 1 < MAX_LEN:
                    checklist.append(index + 1)

                if (index + city.column) < MAX_LEN:
                    checklist.append(index + city.column)

                if index%city.column != 0 and index - 1 > 0:
                    checklist.append(index - 1)

                if (index - city.column) > 0:
                    checklist.append(index - city.column)
                unique = []
                tempscore = 0
                for checkindex in range(len(checklist)):
                    if city.board[checklist[checkindex]] not in unique:
                        unique.append(city.board[checklist[checkindex]])
                        tempscore += 1
                if tempscore > 0:
                    scoring["SHP"].append(tempscore)
                
            elif city.board[index] == 5:
                #EAT SHIT
                if index in parklist:
                    continue
                parklist = countpark(city, index, [])
                scoring["PRK"].append({ 1:1, 2:3, 3:8, 4:16, 5:22, 6:23, 7:24, 8:25 }.get(len(parklist), 25))
            elif city.board[index] == 6:
                if index == 0 or index == city.column - 1 or index == (city.row -1) * city.column or index == MAX_LEN -1:
                    connersquares += 1
                else:
                    nonconnersquares += 1
    scoring["HWY"].append(hwytemp)
    cityscore = 0
    #print stuff..
    print("\nBCH:", end = " ")
    if scoring["BCH"] == []:
        print("0 = 0")
    else:
        for i in range(len(scoring["BCH"]) -1):
            print(scoring["BCH"][i], end = " + ")
        print(scoring["BCH"][-1], end = " = ")
        print(sum(scoring["BCH"]))
        cityscore += sum(scoring["BCH"])

    print("FAC:", end = " ")
    if scoring["FAC"] == 0:
        print("0 = 0")
    else:
        if scoring["FAC"] < 5:
            total  = scoring["FAC"] ** 2
            cityscore += total
            for i in range(scoring["FAC"] -1):
                print(scoring["FAC"], end = " + ")
            print(scoring["FAC"], end = " ")
            print("=", end = " ")
            print(total)
        else:
            total = 1 * (scoring["FAC"] -4) + 16
            cityscore += total
            for i in range(4):
                print(4, end = " + ")
            for i in range(scoring["FAC"] - 5):
                print(1, end = " + ")
            print(1, end = " = ")
            print(total)

    print("HSE:", end = " ")
    if scoring["HSE"] == []:
        print("0 = 0")
    else:
        for i in range(len(scoring["HSE"]) - 1):
            print(scoring["HSE"][i], end = " + ")
        print(scoring["HSE"][-1], end = " = ")
        print(sum(scoring["HSE"]))
        cityscore += sum(scoring["HSE"])

    print("SHP:", end = " ")
    if scoring["SHP"] == []:
        print("0 = 0")
    else:
        for i in range(len(scoring["SHP"]) - 1):
            print(scoring["SHP"][i], end = " + ")
        print(scoring["SHP"][-1], end =  " = ")
        print(sum(scoring["SHP"]))
        cityscore += sum(scoring["SHP"])

    print("HWY:", end = " ")
    if scoring["HWY"] == []:
        print("0 = 0")
    else:
        for i in range(len(scoring["HWY"]) - 1):
            for j in range(scoring["HWY"][i]):
                print(scoring["HWY"][i], end = " + ")
        for i in range(scoring["HWY"][-1] - 1):
            print(scoring["HWY"][-1], end = " + ")
        print(scoring["HWY"][-1], end = " = ")
        print(sum(map(lambda x: x * x, scoring["HWY"])))
        cityscore += sum(map(lambda x: x * x, scoring["HWY"]))

    print("PRK:", end = " ")
    if scoring["PRK"] == []:
        print("0 = 0")
    else:
        for i in range(len(scoring["PRK"]) - 1):
            print(scoring["PRK"][i], end = " + ")
        print(scoring["PRK"][-1], end = " = ")
        print(sum(scoring["PRK"]))
        cityscore += sum(scoring["PRK"])

    print("MON:", end = " ")
    if connersquares == 0 and nonconnersquares == 0:
        print("0 = 0")
    else:
        if connersquares < 3:
            total = 2 * connersquares + nonconnersquares
            cityscore += total
            for i in range(connersquares):
                print(2, end = " + ")
            for i in range(nonconnersquares - 1):
                print(1, end = " + ")
            print(1, end = " = ")
            print(total)
        else:
            total = 4 * (connersquares + nonconnersquares)
            cityscore += total
            for i in range(connersquares + nonconnersquares - 1):
                print(4, end = " + ")
            print(4, end = " = ")
            print(total)
    print("Total score: " + str(cityscore))
    return cityscore

#Check for an index that is -1 (empty space)
def GameisnotFull(city):
    for index in range(city.column * city.row):
        if city.board[index]  < 0:
            return True
    return False

#Main application loop
def main():
    #This is what you get if you don't read the documentations
    if not os.path.exists("highscores\\"):
        os.mkdir(dir_path + "\\highscores\\")
    if not os.path.exists("saves\\"):
        os.mkdir(dir_path + "\\saves\\")
    
    while True:
        print("Welcome, mayor of Simp City!\n" \
              "----------------------------\n" \
              "1. Start new game\n" \
              "2. Load saved game\n" \
              "3. Show high scores\n\n" \
              "0. Exit\n")
        while True:
            choice = input("Your choice? ")
            if len(choice) != 1 or not choice.isdecimal():
                print("Invalid Input!")
                continue
            else:
                choice = int(choice)
                if choice < 0 or choice > 3:
                    print("Invalid Input!")
                    continue
            break
        city, turn, building_pool = None, None, None
        tempchoice = choice
        
        if choice == 0:
            return EXIT_SUCCESS
        elif choice == 1:
            turn, building_pool = 1, {}
            print("\nUsual choices\n" \
                  "-------------\n" \
                  "1. 4 x 4\n" \
                  "2. 5 x 5\n" \
                  "3. 7 x 7\n" \
                  "4. Custom\n\n"\
                  "0. Exit to main menu\n")
            while True:
                choice = input("Your choice? ")
                if len(choice) != 1 or not choice.isdecimal():
                    print("Invalid Input!")
                    continue
                else:
                    choice = int(choice)
                    if choice < 0 or choice > 4:
                        print("Invalid Input!")
                        continue
                break
            if choice == 0:
                print()
                continue
            elif choice == 1:
                city = city_t(4, 4)
            elif choice == 2:
                city = city_t(5, 5)
            elif choice == 3:
                city = city_t(7, 7)
            elif choice == 4: 
                row, column = 0, 0
                while True:                        
                    row = input("Enter the number of rows to start with (must be at least 4): ")

                    if len(row) != 1 or not row.isdecimal():
                        print("Invalid Input!")
                        continue
                    else:
                        row = int(row)
                        if row < 4:
                            print("Invalid Input!")
                            continue
                    break
                while True:
                    column = input("Enter the number of columns to start with (must be at least 4): ")

                    if len(column) != 1 or not column.isdecimal():
                        print("Invalid Input!")
                        continue
                    else:
                        column = int(column)
                        if column < 4:
                            print("Invalid Input!")
                            continue
                    break
                city = city_t(row, column)
            buildingchosen = []
            questions = [0,1,2,3,4,5,6]
            for times in range(5):
                print("\nBuilding chosen for game\n" \
                      "------------------------")
                for i in range(len(buildingchosen)):
                    print("{}. {}".format(i + 1, BWORD[buildingchosen[i]]))
                print()
                
                for i in range(len(questions)):
                    print("{}. {}".format(i + 1, BLONGWORD[questions[i]]), end = "   ")
                print("0.Exit to main menu")
                
                while True:
                    choice = input("\nYour choice? ")
                    if len(choice) != 1 or not choice.isdecimal():
                        print("Invalid Input!")
                        continue
                    else:
                        choice = int(choice)
                        if choice < 0 or choice > len(questions):
                            print("Invalid Input!")
                            continue
                    break
                if choice == 0:
                    print()
                    break
                buildingchosen.append(questions.pop(choice - 1))
            if choice == 0:
                continue
            num_builds = math.floor(math.sqrt(city.column * city.row * 4))
            for i in range(5):
                building_pool[buildingchosen[i]] = num_builds
            print("\nFinal Building Selection\n" \
                  "-------------------------")
            for i in range(len(building_pool)):
                print("{}. {}".format(i + 1, BWORD[buildingchosen[i]]))
            print()
        elif choice == 2:
            while True:
                filename = input("Save filename: ")
                if os.path.exists(saves_path + filename + ".svf"):
                    city, turn, building_pool = read_gamefile(filename + ".svf")
                    break
                else:
                    print("Invalid save filename!")
                    while True:
                        choice = input("Do you want to return menu (y/n)? ")
                        if len(choice) != 1 or not choice.isalpha():
                            print("Invalid Input!")
                            continue
                        else:
                            choice = choice.lower()
                            if choice != "y" and choice != "n":
                                print("Invalid Input!")
                                continue
                        break
                    if choice == 'n':
                        continue
                    print("\n")
                    break
        elif choice == 3:
            print("\n---------- HIGH SCORE CATEGORIES ---------\n")
            categories = os.listdir(highscore_path)
            for i in range(len(categories)):
                print("{}. {}".format(i + 1, categories[i][:-4:]))
            while True:
                choice = input("Your choice? ")

                if not choice.isdecimal():
                    print("Invalid Input!")
                    continue
                else:
                    choice = int(choice)
                    if choice < 1 or choice > len(categories):
                        print("Invalid Input!")
                        continue
                break
            print_highscore(categories[choice -1])
        
        if city == None and city == turn and turn == building_pool:
            if tempchoice == 3:
                continue
            elif tempchoice == 2:
                continue

        while GameisnotFull(city):
            choice1, choice2 = random_select(building_pool), random_select(building_pool)
            while True:
                print_gui(city, turn, building_pool)
                #Print options
                print("\n1. Build a {}\n" \
                         "2. Build a {}\n" \
                         "3. See current score\n" \
                         "4. Save game\n" \
                         "0. Exit to main menu\n".format(BWORD[choice1], BWORD[choice2]))
                while True:
                    choice = input("Your choice? ")
                    if len(choice) != 1 or not choice.isdecimal():
                        print("Invalid Input!")
                        continue
                    else:
                        choice = int(choice)
                        if choice < 0 or choice > 4:
                            print("Invalid Input!")
                            continue
                    break

                if choice == 0:
                    print()
                    break
                elif choice == 1 or choice == 2:
                    while True:
                        buildwhere = input("Build where? ")
                        row, column = None, None
                        try:
                            row, column = buildwhere.split(',')
                            if not row.isdigit() or not column.isdigit():
                                print("Invalid Input!")
                                continue
                            else:
                                buildwhere = int(column)-1 + (int(row) -1) * city.column
                                if buildwhere < 0 or buildwhere > city.column * city.row -1:
                                    print("Choice must be a valid space!")
                                    continue
                                else:
                                    if city.board[buildwhere] != -1:
                                        print("Splace already filled!")
                                        continue
                        except:
                            print("Invalid Input!")
                            continue
                       
                        checklist = []
                        if buildwhere%city.column != city.column - 1 and buildwhere + 1 < city.column * city.row:
                            checklist.append(buildwhere + 1)

                        if (buildwhere + city.column) < city.column * city.row:
                            checklist.append(buildwhere + city.column)

                        if buildwhere%city.column != 0 and buildwhere - 1 > -1:
                            checklist.append(buildwhere - 1)

                        if (buildwhere - city.column) > -1:
                            checklist.append(buildwhere - city.column)

                        if turn != 1:
                            checklen = len(checklist)
                            for index in range(checklen):
                                if city.board[checklist[checklen - index -1]] == -1:
                                    checklist.pop()

                            if checklist == []:
                                print("Building space must be adjacent to existing buildings!")
                                continue
                        break
                    chosen = choice1 if choice == 1 else choice2
                    city.board[buildwhere] = chosen
                    if building_pool[chosen] == 0:
                        building_pool.pop(chosen)
                    break
                elif choice == 3:
                    print_score(city)
                elif choice == 4:
                    while True:
                        filename = input("Input save filename: ")
                        if os.path.exists(saves_path + filename + ".svf"):
                            print("File save already exists!")
                            continue
                        break
                    save_gamefile(filename + ".svf", city, turn, building_pool)
                    break
            if choice == 0 or choice == 4:
                break
            turn += 1
        if choice == 0 or choice == 4:
            continue
        print("\nFinal layout of Simp City:")
        print_squaregrid(city)
        score = print_score(city)
        update_highscore(city.row, city.column, score)
        print()
        
if __name__ == "__main__":
    main()
#Joshua Ng P13, 700+ lines
#Just read with eyes lul
