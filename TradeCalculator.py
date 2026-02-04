"""
Docstring for TradeCalculator:
    A simple trade calculator for seeing who wins a trade between two NFL teams
    that involves only NFL Draft selections, or "picks".

    Author: Brandon Vassallo

"""

import os


"""
THINGS TO STLL DO:

1) Implement a Future Pick ability into total_draft_value()

2) 

3) 

4) Test/Debug the program

"""




#########################################
# FUNC:  reset_Trade_chart              #
#                                       #
# DESCRIPTION:                          #
# Resets the TradeChart.csv file        #
# by using TradeValuesRAW.csv           #
# which should be found in this folder  #
#########################################

def reset_Trade_chart(rawdata_path: str):
    """
    Resets the file TradeChart.csv to its readable form
    
        rawdata (str) --> the file name of the Raw Data file

    """
    ##########################################    
    # Openning files
    ##########################################

    pyfile_dir = os.path.dirname(__file__)                  # Finds the directory that the python file is currently in
    file_TC_path = os.path.join(pyfile_dir, "TradeChart.csv")   # Appends either the raw, or current file name to it

    file_RAW = open(f"{rawdata_path}","r")
    file_TC = open(f"{file_TC_path}","w")

    pick_chart = []

    #########################################################
    # Splitting up each indiviual string into workable rows
    #########################################################

    while cur_line != "":
        cur_line = file_RAW.readline()
        cur_line = cur_line.split()

        '''
        cur_line should now look like: [<pick number>, <team>, <pick value>, <pick number>, <team>, <pick value>, ...etc]
        repeating for every row in the RAW csv file
            Ex: ["1", "CHI", "1000", "33", "BUF, "180", ...]

        The for loop below will seperate the cur_line into the below format:
            [pick, val]
                pick --> The pick number (represented by the f)
                val  --> The value of the pick
            
            Note: The <team> is ignored, as we just want the pick values

            Note: 
                The for loop iterates by 3, as each pick (in it's raw form) is represented by 3 values in the RAW csv:
                    <pick number>, <team>, <pick value>

                We only want the first value (pick, or cur_line[i]) and the third value (val, or cur_line[i+2])
                throwing away the second value (team, or cur_line[i+1] in this case)
        '''

        for i in range(0,len(cur_line),3):
            pick = cur_line[i]
            val = cur_line[i+2]
            pick_chart += [[pick,val]]


    ##########################################    
    # Sorting the picks using bubble sort
    ##########################################

    def bub_sort(list):
        finished = False
        while not finished:     # While the list is not sorted (When finished becomes true in the conditional below, the loop will end)
            finished = True     # Sets the list to finish if no changes are made
            for i in range(len(list)):  # Starts a loop to evaluate the entire list
                if i+1 == len(list):    # If the next index is not defined, ignore any of the code (Helps prevent evaluation of an unidentified index)
                    pass
                elif int(list[i][0]) > int(list[i+1][0]): # If the value is larger than the next value
                    x = list[i]            # This garbage switches the two values
                    list [i] = list[i+1]
                    list[i+1] = x
                    finished = False       # Tells the program to re-evaluate the entire list again
                else:
                    pass
        return list

    sort_picks = bub_sort(pick_chart)

    for i in range(len(sort_picks)):
        file_TC.write(f"{sort_picks[i][0]},{sort_picks[i][1]}\n")
    
    file_RAW.close()
    file_TC.close()


#########################################
# FUNC:  total_draft_value              #
#                                       #
# DESCRIPTION:                          #
# Calculates the total draft            #
# value of all picks involved by one    #
# team in a trade                       #
#########################################

def total_draft_value(refine_fn: str, team: str):

    ##########################################    
    # Fetching the pick value list
    ##########################################

    file_TC = open(f"{refine_fn}","r")
    all_pik_vals = []

    '''
    all_pik_vals is an array of lists, which each list inside the array representing a pick number,
    and it's values as shown below:

        [['1', '1000\n']
         ['2', '717\n"]
         [...]
        ]
    '''

    Fpick_list = [(142, "Future 1st Round Pick"),(57, "Future 2nd Round Pick"),(18, "Future 3rd Round Pick"),
                  (8, "Future 4th Round Pick"),(4, "Future 5th Round Pick"),(1, "Future 6th Round Pick"),
                  (1, "Future 7th Round Pick")]
    line = file_TC.readline()
    while line != "":
        line = line.split(",")
        all_pik_vals += [line]
        line = file_TC.readline()
    picks_confirm = False

    ##########################################
    # Prompting for picks
    ##########################################
    while picks_confirm == False:
        team_picks = []
        team_future_picks = []
        team_future_picks_value = 0
        input_pick = input(f"What pick is {team} willing to trade?\n *For future picks, type FP to prompt the addition of a future pick  ")
        while input_pick != "N":
            if input_pick[0] == "F" and input_pick[1] == "P":         # Is this a future pick?
                future_pick_input = input("What round will this pick be? (Min 1, Max 7, Type 0 to cancel)    ")
                try:
                    future_pick_input = int(future_pick_input)
                    if future_pick_input < 0 or future_pick_input > 7:
                        print()
                        print("Please select a round between 1 and 7")
                        print()    
                        input_pick = "FP"    # Sends the prompt back to asking for what round for the future pick
                    elif future_pick_input == 0:        # An input of 0 canceles the selection of a future pick
                        print()
                        print("FUTURE PICK SELECTION CANCELED")
                    else:
                        team_future_picks += [Fpick_list[future_pick_input-1][1]]
                        team_future_picks_value += Fpick_list[future_pick_input-1][0]
                except ValueError:
                    print()
                    print("The round needs to be a number, dork")
                    print()
                    input_pick = "FP"    # Sends the prompt back to asking for what round for the future pick

                    ''' ######################################### '''
                    '''   NEEDS TO BE IMPLEMENTED: Future Picks   '''
                    ''' ######################################### '''

                

            else:       # Its a regular pick
                try:
                    input_pick = int(input_pick)
                    if input_pick > len(all_pik_vals) or input_pick <= 0:
                        print()
                        print("THIS PICK DOES NOT EXIST")
                        print()
                        input_pick = None
                except ValueError:
                    print()
                    print("The pick needs to be a number, dork")
                    print()
            if input_pick != None and isinstance(input_pick, int):
                team_picks += [input_pick]
            print()
            input_pick = input(f"What other pick is {team} willing to trade? (Respond with N when finished)\n *For future picks, type FP to prompt the addition of a future pick  ")


        ##########################################
        # Calculating the total value of all picks
        ##########################################

        team_tot = 0
        for pik in team_picks:
            
            found = False
            i = 0
            while not found:
                if str(pik) == all_pik_vals[i][0]:      
                    if pik == 257:
                        team_tot = int(all_pik_vals[i][1])              # The pick 257's value string does not have an "\n"
                    else:
                        team_tot += int(all_pik_vals[i][1][:-1])        # The [:-1] will take off the last character in the string, which is "\n"              
                    found = True
                i += 1  
        
        team_picks.extend(team_future_picks)
        team_tot += team_future_picks_value

        """
        USE read_picks() TO DISPLAY THE SELECTED PICKS
            
        """

        read_picks(team_picks)

        ##########################################
        # Confirming the picks selected
        ##########################################

        print("________________________________________________________________")
        confirmation = input(f"Confirm the above picks for the {team}?  [Y, N]:  ")
        final_confirm = False
        while final_confirm == False:
            if confirmation == "Y" or confirmation == "y":
                print()
                print(f"Picks for the {team} CONFIRMED")
                final_confirm = True
                picks_confirm = True
                
            elif confirmation == "N" or confirmation == "n":
                print()
                print("________________________________________________________________")
                print(f"Resetting the picks for the {team}...")
                print("________________________________________________________________")
                print()
                final_confirm = True
                picks_confirm = False

            else:
                print("Please respond with Y or N")
                confirmation = input("[Y, N]:  ")
                final_confirm = False


    file_TC.close()
    return team_tot


#########################################
# FUNC:  calculation                    #
#                                       #
# DESCRIPTION:                          #
# Uses the pick values found by         #
# total_draf_value to find out what     #
# team won in the trade                 #
#########################################

def calculation(refine_fn: str):
    
    file_TC = open(f"{refine_fn}","r")     # Open the pick value file for pick comparison

    print("--------------------------------------------------------------------------")
    print(f"This file is being used for calculating the trades:  {refine_fn}")
    print("--------------------------------------------------------------------------")


    ####################################
    # Prompting for Team 1 picks
    ####################################
    print()
    team1 = input("Please input the first team to participate in the trade:  ")
    print()

    team1_tot = total_draft_value(refine_fn, team1)

    ####################################
    # Prompting for Team 2 picks
    ####################################
    print()
    team2 = input("Please input the second team to participate in the trade:  ")
    print()

    team2_tot = total_draft_value(refine_fn, team2)

    ####################################
    # Who wins?
    ####################################
    pick_dif = team1_tot - team2_tot
    
    if pick_dif != 0:
        if pick_dif > 0:
            winning_team = team1
        else:
            winning_team = team2
        print(f"\n{winning_team} wins the trade with {abs(pick_dif)} points in difference")
        print("\nThis is equivalent to the below package:")
        tie = False
    else:
        print()
        print("----------------------------------------------------------------")
        print(f"\nThis trade is perfectly symetrical, no one wins and no one loses")
        print("----------------------------------------------------------------")
        print()
        tie = True

    ####################################
    # By how much?
    ####################################
    if not tie:
        pick_val_line = file_TC.readline()   
        pick_val = pick_val_line.split(",")     # AN ARRAY: [Pick #, Pick Value]
        future_pick_list = [(18, "Future 3rd Round Pick"),(8, "Future 4th Round Pick"), (4, "Future 5th Round Pick"),(1, "Future 6th/7th Round Pick")] 
        picks_finished = False
        curr_pick_dif = abs(pick_dif)
        total_pick_dif_nums = []

        # Find the value of the pick(s) that represents the winning difference
        while not picks_finished:
            if curr_pick_dif == 0:
                picks_finished = True

            elif curr_pick_dif >= int(pick_val[1][:-1]):
                # We can use the current pick to represent some of the pick differential
                # Add the current pick_val's pick number to the total_pick_dif_nums array and
                # Subtract the pick_val's pick value from the curr_pick_dif
                if curr_pick_dif <= 20:
                    # If the current pick differential value is less than or equal to 20, we should use
                    # future picks instead of current picks, as duplicate pick values begin to show up around this area.
                    for future_pick in future_pick_list:
                        if curr_pick_dif >= future_pick[0]:
                            total_pick_dif_nums += [future_pick[1]]
                            curr_pick_dif -= future_pick[0]
                else:
                    total_pick_dif_nums += [int(pick_val[0])]
                    curr_pick_dif -= int(pick_val[1][:-1])
                
            else:
                # The current state of the pick differential constant is too small to subtract any more picks
                # Therefore, use readline() to move onto the next pick
                pick_val_line = file_TC.readline()
                pick_val = pick_val_line.split(",")     # AN ARRAY: [Pick #, Pick Value]

        """
        USE read_picks() TO DISPLAY THE PICK DIFFERENCE
        
        """

        read_picks(total_pick_dif_nums)

    file_TC.close()


#########################################
# FUNC:  read_picks                     #
#                                       #
# DESCRIPTION:                          #
# Takes in an array full of pick        #
# numbers and outputs them according    #
# to their round                        #
#########################################

def read_picks(picks: list):

    ''' 
    IMPLIMENTATION NOTES:
        1) The picks in the "picks" list will be integers if they are specific picks, but strings if they are future picks.
        The strings provided by future picks should simply be displayed if they are found within the picks array

        2) The pick discrestion should be as follows:
            Round 1: 1-32
            Round 2: 33-64
            Round 3: 65-102
            Round 4: 103-138
            Anything beyond Round 4 should be referenced as future picks (*see calculation method)

    '''
    
    ####################################
    # Split the lists into current and
    # future picks for sorting
    ####################################
    
    current_picks = []
    future_picks = []
    error_picks = []
    for pick in picks:
        if isinstance(pick, str):       # The pick is a future pick
            future_picks += [pick]
        elif isinstance(pick, int):
            current_picks += [pick]
        else:
            error_picks += [f"ERROR: This pick, [{pick}] is not valid"]

    ####################################
    # Sort each list
    ####################################

    current_picks.sort()

    finished = False
    while not finished:                             # While the list is not sorted (When finished becomes true in the conditional below, the loop will end)
        finished = True                             # Sets the list to finish if no changes are made
        for i in range(len(future_picks)):          # Starts a loop to evaluate the entire list
            if len(future_picks[i]) == 25:
                future_pick_number = int(future_picks[i][7:-17])       # Isolates the future pick number
            else:
                future_pick_number = int(future_picks[i][7:-13])       # Isolates the future pick number
            if i+1 == len(future_picks):                    # If the next index is not defined, ignore any of the code (Helps prevent evaluation of an unidentified index)
                pass
            elif future_pick_number > int(future_picks[i+1][7:-13]): # If the value is larger than the next value
                x = future_picks[i]                         # This garbage switches the two values
                future_picks [i] = future_picks[i+1]
                future_picks[i+1] = x
                finished = False                    # Tells the program to re-evaluate the entire list again
            else:
                pass

    ####################################
    # Add the Pick Rounds into the full
    # print array
    ####################################

    print_array = []
    for pick in current_picks:
        if pick <= 32:
            print_array += [f"[{pick}] --> No. {pick} in the 1st round"]
        elif pick <= 64:
            print_array += [f"[{pick}] --> No. {pick-32} in the 2nd round"]
        elif pick <= 102:
            print_array += [f"[{pick}] --> No. {pick-64} in the 3rd round"]
        elif pick <= 138:
            print_array += [f"[{pick}] --> No. {pick-102} in the 4th round"]
        elif pick <= 176:
            print_array += [f"[{pick}] --> No. {pick-138} in the 5th round"]
        elif pick <= 216:
            print_array += [f"[{pick}] --> No. {pick-176} in the 6th round"]
        else:
            print_array += [f"[{pick}] --> No. {pick-216} in the 7th round"]

    print_array.extend(future_picks)
    print_array.extend(error_picks)

    print()
    print("----------------------------------------------------------------")
    print("TOTAL PACKAGE:")
    print()

    for pick_str in print_array:
        print(pick_str + "\n")

    print()
    print("----------------------------------------------------------------")
    print()

def main():

    start = input("TRADE CALCULATOR 1.0   ")
    pyfile_dir = os.path.dirname(__file__)          # Finds the directory that the python file is currently in
    if start == "RESET":
        print("Make sure your files are in the folder: TradeCalculator, and has no commas")
        print("A File named TradeChart.csv will be overwritten if it exists")
        start = input("Are you sure you want to reset the file TradeChart.csv? Y/N   ")
        checked = False
        while not checked:
            if start == "Y":

                raw = input("RAW DATA FILE NAME:   ")
                full_file_RAW_path = pyfile_dir.join(raw)       # Appends the data file into the datapath

                reset_Trade_chart(full_file_RAW_path)

                print()
                print("FINISHED RESET")
                print()
                print("Begining program...")
                print()
                checked = True
            elif start == "N":
                print()
                print("OK, begining program...")
                print()
                checked = True
            else:
                print("NOT A VALID ANSWER")

    full_file_TC_path = os.path.join(pyfile_dir, "TradeChart.csv")   # Appends either the raw, or current file name to it
    calculation(full_file_TC_path)
    print()
    print("Press any key to continue...")
    input()         # Pauses the program and waits for user input


if __name__ == "__main__":
    main()
    