import datetime

"""
getDate is used by getDictionary to build the datetime object
from the string that the csv file provides
@param string to convert to date (from csv data file)
@returns datetime object
@throws TypeError
Author: Elliot Winch
Date: 2017-14-10        
"""          
def getDate(string):
    try:
        month = getMonth(string[:3])
        day = int(string[4:6])
        year = int(string[8:12])
    except TypeError:
        raise
    
    return datetime.date(year, month, day)
  
months = { 
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12 }  

"""
getMonth is a helper method for getDate.
@param string to test as month 
@returns int from 1 - 12 representing month
@throws TypeError
Author: Elliot Winch
Date: 2017-14-10        
"""     
def getMonth(monthString):
    if monthString in months:
        return months[monthString]
    else:
raise TypeError