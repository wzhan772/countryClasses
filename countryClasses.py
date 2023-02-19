'''
processUpdates takes into from the update files and sorts them to be either valid or invalid
valid updates are then implemented into the data file, whereas invalid ones are written into the badupdates file
'''
from catalogue import countryCatalogue
from country import Country
import os.path

def processUpdates(cntryFileName, updateFileName, badUpdateFile):

    result = True
    catlog = None
    fileFoundD = False
    fileFoundU = False

    #verifying each data and update file
    while not fileFoundD:
        if os.path.isfile(cntryFileName):
            fileFoundD = True
        else:
            countryInput = input('The data file does not exist: Quit? Y=yes/N=no : ')
            if countryInput == 'N' or countryInput == 'n':
                cntryFileName = input('Enter file with data : ')
            else:
                output_file = open('output.txt', 'w')
                output_file.write('Update Unsuccessful\n')
                output_file.close()
                result = False
                return (result, catlog)
    while not fileFoundU:
        if os.path.isfile(updateFileName):
            fileFoundU = True
        else:
            updateInput = input('The update file does not exist OR Type "N" and key in new update file: Quit? Y=yes/N=no : ')
            if updateInput == 'N' or updateInput == 'n':
                updateFileName = input('Enter file with updates : ')
            else:
                output_file = open('output.txt', 'w')
                output_file.write('Update Unsuccessful\n')
                output_file.close()
                result = False
                return (result, catlog)

    badUpdates = open(badUpdateFile, "w")
    fileToUpdate = open(updateFileName, "r")
    catlog = countryCatalogue(cntryFileName)
    contList = ["Africa", "Antarctica", "Arctic", "Asia", "Europe", "North_America", "South_America"]

    #split each line in the update file by semicolons
    for element in fileToUpdate:
        changedElement = element.split(";")
        changedFinalElement = []
        checkIfValid = True

        #join each element by each space in a new list
        for combinedElement in changedElement:
            newList = "".join(combinedElement.strip())
            changedFinalElement.append(newList)

        #if the element is empty, write it into the badupdates file
        for space in changedElement:
            if space == "":
                badUpdates.write(element)
                checkIfValid = False

        countryName = changedFinalElement[0]
        #if the element is empty, write it into the badupdates file
        for space in countryName:
            if space == " ":
                badUpdates.write(element)
                checkIfValid = False

        #check for valid country index
        if len(changedFinalElement) > 1:
            updateMade = changedFinalElement[1:]
        else:
            updateMade = ""

        #check if country is named correctly
        countryCheck = countryName.split("_")
        for i in range(len(countryCheck)-1):
            if not countryCheck[i][0].isupper():
                badUpdates.write(element)
                checkIfValid = False
            if countryCheck == "":
                badUpdates.write(element)
                checkIfValid = False

        #check number of times P, A, or C occurs in one line
        numberofP = 0
        numberofA = 0
        numberofC = 0
        #check to see if each update numbers and continents are valid, if they are not add to badupdates file
        for updateLine in updateMade:
            if updateLine[0:2] == "P=":
                changedUpdate = (updateLine.split(","))
                changedUpdate[0] = changedUpdate[0][2:]
                numberofP += 1
                if len(changedUpdate[0]) > 3:
                    badUpdates.write(element)
                    checkIfValid = False
                nextUpdate = changedUpdate[1:]
                for updateLine in nextUpdate:
                    if (len(updateLine) != 3):
                        badUpdates.write(element)
                        checkIfValid = False

            elif updateLine[0:2] == "A=":
                changedUpdate = (updateLine.split(","))
                changedUpdate[0] = changedUpdate[0][2:]
                numberofA += 1
                if len(changedUpdate[0]) > 3:
                    badUpdates.write(element)
                    checkIfValid = False
                nextUpdate = changedUpdate[1:]
                for updateLine in nextUpdate:
                    if (len(updateLine) != 3):
                        badUpdates.write(element)
                        checkIfValid = False

            elif updateLine[0:2] == "C=":
                numberofC += 1
                if updateLine not in contList:
                    badUpdates.write(element)
                    checkIfValid = False
            else:
                badUpdates.write(element)
                checkIfValid = False

        #checks to see if updates are empty or if number of updates exceeds four, or if number of P,A,C is more than once in a line
        if updateMade == "" or len(changedFinalElement) > 4 or numberofC > 1 or numberofP > 1 or numberofA > 1:
            badUpdates.write(element)
            checkIfValid = False

        #if the update is valid then add it to each updated P, A, and C
        if checkIfValid == True:
            index = "=".join(updateMade)
            indexUpdate = index.split("=")
            updatedCount = Country()
            updatedCount.setName(countryName)

            for i in range(len(indexUpdate)):
                #if index is C and if the update is not None, get the new update
                if indexUpdate[i] == "C":
                    updateContinent = indexUpdate[i + 1]
                    updatedCount.setContinent(updateContinent)
                    if catlog.findCountry(updatedCount.getName()) != None:
                        catlog._countryCat[updatedCount.getName()][0] = updatedCount.getContinent()
                    else:
                        catlog.addCountry(updatedCount.getName(), updatedCount.getPopulation(), updatedCount.getArea(), updatedCount.getContinent())
                        catlog._countryCat[updatedCount.getName()][0] = updatedCount.getContinent()
                #if index is P and if the update is not None, get the new update
                elif indexUpdate[i] == "P":
                    updatePopulation = indexUpdate[i + 1]
                    updatedCount.setPopulation(updatePopulation)
                    if catlog.findCountry(updatedCount.getName()) != None:
                        catlog._countryCat[updatedCount.getName()][1] = updatedCount.getPopulation()
                    else:
                        catlog.addCountry(updatedCount.getName(), updatedCount.getPopulation(), updatedCount.getArea(), updatedCount.getContinent())
                #if index is A and if the update is not None, get the new update
                elif indexUpdate[i] == "A":
                    updateArea = indexUpdate[i + 1]
                    updatedCount.setArea(updateArea)
                    if catlog.findCountry(updatedCount.getName()) != None:
                        catlog._countryCat[updatedCount.getName()][2] = updatedCount.getArea()
                    else:
                        catlog.addCountry(updatedCount.getName(), updatedCount.getPopulation(), updatedCount.getArea(), updatedCount.getContinent())
    #call save function to save each update
    catlog.saveCountryCatalogue("output.txt")
    #return the results
    return (result, catlog)
