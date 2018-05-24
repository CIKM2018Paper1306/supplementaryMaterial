import argparse
import pandas as pd
import fleisskappa as fk
import os


#parameter that saves at which column the actual data begin
column = None

#paramater that saves the name of the evaluation file
resultName = ""

#dictionary containing the line Strings of each participant: key - participant ID
persIDdict = dict()

#Method for the Command Line Interface, arguments: -f (input file/files), -c (input column of data begin)
#return: A dictionary containing another dictionary of each column of each file: first key - file name, second key - column name (first line)
def commandLine():
    
    global column
    global resultName
    global persIDdict
    
    #set CLI commands
    parser = argparse.ArgumentParser(description="Evaluate the contents of a LSG-Result file.")
    parser.add_argument("-f", "--file", help="Input path to CSV-Result file", required=True, nargs="*")
    parser.add_argument("-c", "--col", help="Choose at which column the actual result data begin", required=True)
    
    #parse arguments
    args = parser.parse_args()
    #get the path of each file saved in a list
    csv_files = args.file
    #set the column number at which the actual data begin
    column = int(args.col)
    
    #initializing survey dictionary
    surveys = {}
    #loop over each file path in the file list
    for csv_file in csv_files:
        
        #set name of the evaluation file with the names of the individual file separated with "__"
        resultName = resultName + "__" + os.path.splitext(csv_file)[-2]
        #pandas module: fill the survey dictionary with the column dictionary of the files. The pandas module goes
        #through the first line of the CSV file and takes each field as the keys for the column dictionary
        surveys[csv_file] = pd.read_csv(csv_file, sep=",")
        
        for persID in surveys[csv_file]["id. Response ID"]:
            
            persIDdict[persID] = "Rater " + str(persID)
            
    
    #return the survey dictionary
    return surveys
    



def buildKrippendorffMatrix(surveys):
    
    #dictionary containing the IDs for each category: key - category name
    categories = {}
    categories["Organism"] = 1
    categories["Environment"] = 2
    categories["Quality"] = 3
    categories["Mat & Subst"] = 4
    categories["Method"] = 5
    categories["Data Type"] = 6
    categories["Process"] = 7
    categories["Anatomy"] = 8
    categories["Location"] = 9
    categories["Time"] = 10
    categories["Event"] = 11
    categories["Person & Org"] = 12
    categories["Human Inter"] = 13
    categories["Other"] = 14
    categories["None"] = 15
    
    #get the name of the first input survey
    surveyName = list(surveys)[0]
    #get the first input survey
    survey = surveys[surveyName]
    #initialize counting the current column number
    currentColumn = 0
    #number of term
    termNumber = 1
    #String for the first line of the Krippendorff CSV file
    firstTop = "Rater"
    #String for the second line of the Krippendorff CSV file
    secondTop = ""
    #String for the next-to-last line of the Krippendorff CSV file
    firstBottom = "Organism,Environment,Quality,Mat & Subst,Method,Data Type,Process,Anatomy,Location,Time,Event,Person & Org,Human Inter,Other,None"
    #String for the line of the Krippendorff CSV file
    secondBottom = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15"
    #initialize counting the current column number
    currentColumn = 0
    
    #loop over each question and noun of the first input survey --> first key
    for term in survey:
        
        #check if the question starts with the String 'researchfield'. If it does, leave the loop
        #--> end of the actual data in the file
        if(term.lower().startswith("researchfield")):
            break
        
        #check if the current column number is equal or greater than the user set column number (begin of actual data).
        #If it does, start parsing the data of the file. Else, continue to the next column and check again
        if(currentColumn >= column):
            #get the title name
            title = term.split(".")[0].split("[")[0]
            #check if the question is an 'other' of comment section. If it is, ignore this question and noun
            #and continue to the next question and/or noun. Else, parse the question and noun
            if(title[-1] == "C" or title[-2:] == "CQ"):
                continue
            else:
                #get the noun
                noun = term.split("].")[1].split("[")[1][:-1].replace(",", ";")
                firstTop = firstTop + ",<title>-Term" + str(termNumber)
                #increase the term number by 1        
                termNumber = termNumber + 1
                secondTop = secondTop + "," +  title + "-" + noun
                
                #loop over each participant ID
                for persID in persIDdict:
                    
                    #loop over each survey of the survey dictionary
                    for surveyKey in surveys:
                        
                        #initialize the category String
                        category = ""
                        #get the list of participant IDs
                        persIDs = surveys[surveyKey]["id. Response ID"]
                        #initialize index of participant ID
                        surveyIDindex = None
                        #check if the survey contain the participant ID. If it does, get the index of the participant ID.
                        #Else, continue to the next survey
                        if(persID in persIDs.tolist()):
                            surveyIDindex = persIDs[persIDs == persID].index[0]
                        else:
                            continue
                        
                        #get the answer    
                        answer = str(surveys[surveyKey][term][surveyIDindex])
                        #if the answer is 'other', set the category String to 'Other'.
                        if(answer.startswith("<div>other")):
                            category = "Other"
                        #if the answer is empty (no answer was given/NaN), set the category String to 'None'.
                        #Else, set the category String to the answer given by the survey
                        elif(answer == "nan"):
                            category = "None"
                        else:
                            category = answer.split("</span>")[0].split(">")[-1]
                        
                        #append the line String of each participant by the category ID
                        persIDdict[persID] = persIDdict[persID] + "," + str(categories[category])
        
        
        #increase the current column number by 1        
        currentColumn = currentColumn + 1
        
        
        
    summary = ""
    for persID in persIDdict:
        
        summary = summary + persIDdict[persID] + "\n"
        
    #writes the formatted results to the Krippendorff CSV file
    with open("lsg__krippendorff__" + resultName + ".csv", "w") as lsg:
        lsg.write(firstTop + "\n" + secondTop + "\n" + summary + "\n\n\n" + firstBottom + "\n" + secondBottom) 
                        
    
    




#Main method for parsing the Result-CSV file and building the matrix
def startMatrixBuilding():
    
    surveys = commandLine()
    buildKrippendorffMatrix(surveys)
    
    
startMatrixBuilding()
