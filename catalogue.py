'''
class countryCatalogue alters the information about each country by setting, adding, saving, and printing after alteration
Created by: William Zhang
SN: 251215208
'''
from country import Country

class countryCatalogue:
    def __init__(self, countryFile):
        fileInput = open(countryFile, "r")
        #bypass header
        line = fileInput.readline()
        self._countryCat = {}
        #for every element split it by | and set each value
        for element in fileInput:
            element = element.split("|")
            countryAspect = Country()
            countryAspect.setName(element[0].strip()), countryAspect.setContinent(element[1].strip()), countryAspect.setPopulation(element[2].strip()), countryAspect.setArea(element[3].strip())
            self._countryCat[countryAspect.getName()] = [countryAspect.getContinent(), countryAspect.getPopulation(), countryAspect.getArea()]
    #set each continent
    def setContinentOfCountry(self, countryContinents):
        self.countryContinents = countryContinents
    #set each population
    def setPopulationOfCountry(self, countryPopulations):
        self.countryPopulations = countryPopulations
    #set each area
    def setAreaOfCountry(self, countryAreas):
        self.countryAreas = countryAreas
    #match each country
    def findCountry(self, country):
        for determineCountry in self._countryCat:
            if determineCountry == country:
                return country
        return None
    #add each country
    def addCountry(self, countryName, pop, area, cont):
        country = Country(countryName, pop, area, cont)
        if self.findCountry(country) is None:
            self._countryCat[countryName] = [cont, pop, area]
            return True
        else:
            return False
    #print the countries
    def printCountryCatalogue(self):
        for position in self._countryCat:
            country = Country()
            country.setName(position), country.setPopulation(self._countryCat[position][1]), country.setArea(self._countryCat[position][2]), country.setContinent(self._countryCat[position][0])
            country.__repr__()
    #save the countries
    def saveCountryCatalogue(self, fname):
        try:
            file = open(fname, "w")
            file.write("Country|Continent|Population|Area")
            file.write("\n")
            numItems = 0

            for i in sorted(self._countryCat):
                self.setPopulationOfCountry(self._countryCat[i][1])
                self.setAreaOfCountry(self._countryCat[i][2])
                self.setContinentOfCountry(self._countryCat[i][0])

                file.write(i + "|" + self.countryContinents + "|" + self.countryPopulations + "|" + self.countryAreas)
                file.write("\n")

                numItems += 1
            return numItems
        except:
            return -1
