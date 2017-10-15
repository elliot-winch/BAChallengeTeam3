#Extracts the crypto data from the provided csv files 

#Author: Elliot Winch 


import csv
import DateExtractor as de
import SQLForCSVData as sqlcvs

"""
getDatabase returns a SQL database of all the valid entries.

Use getEntries to retreive all entries in a list.

@param relative path to a csv file with appropriate data

@returns SQl database

Author: Elliot Winch
Date: 2017-14-10
"""
def getDatabase(csvFilePath):
    with open(csvFilePath, 'r') as csvFile:
        csvreader = csv.reader(csvFile, delimiter = ",")
        database = sqlcvs.Database(csvreader)
    return database
"""
getList can be called on a relative file path for any
of the provided csv data files.

It will return a list of ALL rows from the data file. 
It is up to the user to determine which rows they will need
(i.e. many of the files have the first row with column headings,
which are likely not desired).

To access an entry in the list, provide an index i, and the
i^th entry in the list will be returned.

@param relative path to a csv file with appropriate data

@returns array with all entries from csv file

Author: Elliot Winch
Date: 2017-14-10
"""   
def getList(csvFilePath):
    valueList = []
    
    with open(csvFilePath, 'r') as csvFile:
        csvreader = csv.reader(csvFile, delimiter = ",")
        
        for row in csvreader:
            valueList.append(row)
            
    return valueList
    
    
"""
getDictionary can be called on a relative file path for any
of the provided csv data files.

It will return a dictionary, key type datetime and value type
array (of all the entries except date).

To access a value in the returned dictionary, index the dictionary
with a datetime object of the date you desire.

@param relative path to a csv file with appropriate data

@returns dictionary with all valid entries from csv file

Author: Elliot Winch
Date: 2017-14-10
"""
def getDictionary(csvFilePath): 
    dictionary = {}
    
    with open(csvFilePath, 'r') as csvFile:
        csvreader = csv.reader(csvFile, delimiter = ",")
                
        for row in csvreader:
            try:
                date = de.getDate(row[0])
                dictionary[date] = row[1:]
            except TypeError:
                continue
                
    return dictionary
                    
                    
if __name__ == "__main__":
    getDatabase("Data/bitcoin_price.csv")