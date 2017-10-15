import sqlite3

"""
Author: Elliot Winch
Date: 2017-10-14
"""
class Database():
    #Instance variables
    databaseName = 'csvdb'
    columnNames = []
    columnNamesString = ''
    db = sqlite3.connect('csvdb.db');
    
    """
    Instaniate method for database. It will call addEntries to
    build the database. 
    
    @param csvreader built from a csv file path
    @optional param string database name
    """
    def __init__(self, csvreader, dbname=databaseName):        
        self.databaseName = dbname
        self.db.text_factory = str
        self.db.row_factory = sqlite3.Row
        self.db.execute('drop table if exists ' + dbname)
         
        self.columnNamesString += ' ('
        createArg = 'create table ' + dbname + ' ( '
        
        columnHeads = csvreader.next()
        numColumnHeads = len(columnHeads) 
        
        for i in range(0, numColumnHeads):
            columnHeads[i] = columnHeads[i].replace(" ","_")
            self.columnNames.append(columnHeads[i])
            self.columnNamesString += columnHeads[i]

            createArg += columnHeads[i] + ' int'

            if(i < numColumnHeads - 1):
                createArg += ', '
                self.columnNamesString += ', '

        
        createArg += ')'
        self.columnNamesString += ') '
    
        self.db.execute(createArg)
        
        self.addEntries(csvreader)
     
    """
    Helper method for __init__. Builts the database from the csvreader
    
    @param csvreader builts from csv file path
    """   
    def addEntries(self, csvreader):
        for rows in csvreader:
            self.addEntry(rows)
        
        self.db.commit()

    """
    Helper method for addEntries. Builds an argument string and sends it
    to the database to add a single entry.
    
    @param csvreader builts from csv file path
    """     
    def addEntry(self, values):        
        insertArg = 'insert into ' + self.databaseName + self.columnNamesString + 'values '
        
        valueString = '('
        
        for i in range(0, len(self.columnNames)):
            valueString += '"' + values[i] + '"'
            
            if(i < len(self.columnNames) - 1):
                valueString += ','
        
        valueString += ')'
        try:
            self.db.execute(insertArg + valueString)
        except Exception:
            return
     
    """
    D A N G E R B O I
    
    Directly pass a command to the database. With great power, comes
    great responcibility.
    
    @param string argument to feed to database
    """                                     
    def passCommand(self, commandString):
        if(commandString[:4] == 'DROP'):
            print 'Not today, Satan.'
        else:
            self.db.execute(commandString)
        
    """
    Builds a SELECT command and returns a list of all the entries.
    
    @optional param string 'orderby': if the pass string is a column
    title, it will order the returned list by this column head. If it
    is invalid, nothing will be returned. bool 'orderbydesc': if true,
    the list will be in descending order (highest value first). string
    'columns': providing a string with valid column titles will return only 
    those columns. 
    """         
    def getEntries(self, orderby = 'Date', orderbydesc = 0, columns = '*'):
        allEntries = []
        if(columns == '*'):
            for i in self.db.execute('select * from ' + self.databaseName + ' order by {}'.format(orderby)):    
                allEntries.append(i)
            return allEntries
        elif (orderby in self.columnNames):
            colargs = ''  
            for arg in columns:
                if(arg in self.columnNames):
                    colargs += '[' + arg + '] '
            
            cmd = 'select ' + colargs + ' from ' + self.databaseName + ' order by {}'.format(orderby)
        
            if(orderbydesc):
                cmd += ' desc'
            
            return self.db.execute(cmd) 