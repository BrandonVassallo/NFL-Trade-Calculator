"""
Docstring for TradeCalculator:
    A simple trade calculator for seeing who wins a trade between two NFL teams
    that involves only NFL Draft selections, or "picks".

    Author: Brandon Vassallo

"""



"""
THINGS TO STLL DO:

1) Implement a Future Pick ability into total_draft_value()

2) Implement the read_picks() method, and add its calls where necessary

3) Fix the open() methods

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

def reset_Trade_chart(rawdata: str):
    """
    Resets the file TradeChart.csv to its readable form
    
        rawdata (str) --> the file name of the Raw Data file

    """
    ##########################################    
    # Openning files
    ##########################################

    file_f = open(f"TradeCalculator\\{rawdata}","r")
    file_TC = open(f"TradeCalculator\\TradeChart.csv","w")

    pick_chart = []

    #########################################################
    # Splitting up each indiviual string into workable rows
    #########################################################

    while cur_line != "":
        cur_line = file_f.readline()
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

    def sort(list):
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

    sort_picks = sort(pick_chart)

    for i in range(len(sort_picks)):
        file_TC.write(f"{sort_picks[i][0]},{sort_picks[i][1]}\n")
    
    file_f.close()
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

    file_TC = open(f"TradeCalculator\\{refine_fn}","r")
    all_pik_vals = []
    Fpick_list = [142,57,18,8,4,1,1]
    line = file_TC.readline()
    while line != "":
        line = line.split(",")
        all_pik_vals += [line]
    picks_confirm = False

    ##########################################
    # Prompting for picks
    ##########################################
    while picks_confirm == False:
        team_picks = []
        input_pick = input(f"What pick is {team} willing to trade?\n *For future picks, type FP to prompt the addition of a future pick  ")
        while input_pick != "N":
            if input_pick[0] == "F" and input_pick[1] == "P":         # Is this a future pick?
                Fpick1 = input("What round will this pick be? (Min 1, Max 7, Type 0 to cancel)    ")
                try:
                    int(Fpick1)
                    
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
                    int(input_pick)
                    if input_pick >= len(all_pik_vals) or input_pick <= 0:
                        print()
                        print("THIS PICK DOES NOT EXIST")
                        print()
                        input_pick = None
                except ValueError:
                    print()
                    print("The pick needs to be a number, dork")
                    print()
            if input_pick != None:
                team_picks += [input_pick]
            print()
            input_pick = input(f"What other pick is {team} willing to trade? (Respond with N when finished)\n *For future picks, type FP to prompt the addition of a future pick  ")

        """
        USE read_picks() TO DISPLAY THE SELECTED PICKS
            
        """

        ##########################################
        # Calculating the total value of all picks
        ##########################################

        team_tot = 0
        for pik in team_picks:
            found = False
            i = 0
            while not found:
                if pik == all_pik_vals[i][0]:
                    team_tot += int(all_pik_vals[i][1])
                    found = True
                i += 1  

        ##########################################
        # Confirming the picks selected
        ##########################################

        print("________________________________________________________________")
        confirmation = input(f"Confirm the above picks for the {team}?  [Y, N]:  ")
        final_confirm = False
        while final_confirm == False:
            if confirmation == "Y" or confirmation == "y":
                print(f"Picks for the {team} CONFIRMED")
                final_confirm = True
                picks_confirm = True
                
            elif confirmation == "N" or confirmation == "n":
                print(f"Resetting the picks for the {team}...")
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
    
    file_TC = open(f"TradeCalculator\\{refine_fn}","r")     # Open the pick value file for pick comparison

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
        print(f"{winning_team} wins the trade with {pick_dif} points in difference")
        tie = False
    else:
        print(f"This trade is perfectly symetrical, no one wins and no one loses")
        tie = True

    ####################################
    # By how much?
    ####################################
    if not tie:
        pick_val = file_TC.readline()   # AN ARRAY: [Pick #, Pick Value]
        future_pick_list = [(18, "Future 3rd Round Pick"),(8, "Future 4th Round Pick"), (4, "Future 5th Round Pick"),(1, "Future 6th/7th Round Pick")] 
        picks_finished = False
        curr_pick_dif = pick_dif
        total_pick_dif_nums = []

        # Find the value of the pick(s) that represents the winning difference
        while not picks_finished:
            if curr_pick_dif == 0:
                picks_finished = True

            elif curr_pick_dif >= pick_val[1]:
                # We can use the current pick to represent some of the pick differential
                # Add the current pick_val's pick number to the total_pick_dif_nums array and
                # Subtract the pick_val's pick value from the curr_pick_dif
                if curr_pick_dif <= 20:
                    # If the current pick differential value is less than or equal to 20, we should use
                    # future picks instead of current picks, as duplicate pick values begin to show up around this area.
                    for future_pick in future_pick_list:
                        if curr_pick_dif >= future_pick[0]:
                            total_pick_dif_nums += future_pick[1]
                            curr_pick_dif -= future_pick[0]
                else:
                    total_pick_dif_nums += pick_val[0]
                    curr_pick_dif -= pick_val[1]
                
            else:
                # The current state of the pick differential constant is too small to subtract any more picks
                # Therefore, use readline() to move onto the next pick
                pick_val = file_TC.readline()

        """
        USE read_picks() TO DISPLAY THE PICK DIFFERENCE
        
        """

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
    FUTURE IMPLIMENTATION NOTES:
        1) The picks in the "picks" list will be integers if they are specific picks, but strings if they are future picks.
        The strings provided by future picks should simply be displayed if they are found within the picks array

        2) The pick discrestion should be as follows:
            Round 1: 1-32
            Round 2: 33-64
            Round 3: 65-102
            Round 4: 103-138
            Anything beyond Round 4 should be referenced as future picks (*see calculation method)

    '''

    pass

def main():
    start = input("TRADE CALCULATOR 1.0   ")
    if start == "RESET":
        print("Make sure your files are in the folder: TradeCalculator, and has no commas")
        print("A File named TradeChart.csv will be overwritten if it exists")
        start = input("Are you sure you want to reset the file TradeChart.csv? Y/N   ")
        checked = False
        while not checked:
            if start == "Y":
                raw = input("RAW DATA FILE NAME:   ")
                reset_Trade_chart(raw)
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
    calculation("TradeChart.csv")


if __name__ == "__main__":
    main()
    