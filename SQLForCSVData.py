import sqlite3

class Database():
    databaseName = 'csvdb'
    columnNames = []
    columnNamesString = ''
    db = sqlite3.connect('csvdb.db');
    
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
        
    def addEntries(self, csvreader):
        for rows in csvreader:
            self.addEntry(rows)
        
        self.db.commit()

        
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
     
                                         
    def passCommand(self, commandString):
        if(commandString[:4] == 'DROP'):
            print 'Not today, Satan.'
        else:
            self.db.execute(commandString)
        
              
    def getEntries(self, orderby = 'Date', orderbydesc = 0, columns = '*'):
        allEntries = []
        if(columns == '*'):
            for i in self.db.execute('select * from ' + self.databaseName + ' order by {}'.format(orderby)):    
                allEntries.append(i)
            return allEntries
        else:
            colargs = ''  
            for arg in columns:
                colargs += '[' + arg + '] '
            
            cmd = 'select ' + colargs + ' from ' + self.databaseName + ' order by {}'.format(orderby)
        
            if(orderbydesc):
                cmd += ' desc'
            
            return self.db.execute(cmd)   