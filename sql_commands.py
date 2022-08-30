import PySimpleGUI as sg
import pyodbc 

def connectToSQL():
    try:
        conn = pyodbc.connect('DRIVER={SQL Server Native Client RDA 11.0};' +
        'SERVER=LAPTOP-MCSMVDLL;' +
        'DATABASE=Магазин_дисков;' +
        'Trusted_Connection=yes;')
    except Exception as error:
        return 'error'
    
    return conn.cursor()

def executeSQL(cursor, command):
    try:
        cursor.execute(command)
    except Exception as error:
        return 'error'
    
    return cursor.fetchone()

def executeSQLAll(cursor, command):
    try:
        cursor.execute(command)
    except Exception as error:
        return 'error'
    
    return cursor.fetchall()

def executeSQLUpdate(cursor, command):
    try:
        cursor.execute(command)
    except Exception as error:
        return 'error'
    
    return 'success'
    
def getUserID(cursor, values):
    return executeSQL(cursor, "select [id_работника]" +
        "from [dbo].[Работник_Логин]" +
        "where ([логин] = '{}' and [пароль] = '{}')".format(values[0], values[1]))

def getUserJob(cursor, userID):
    return executeSQL(cursor, "select [id_должности]" +
        "from [dbo].[Работник_Должность]" +
        "where [id_работника] = '{}'".format(userID))

def getUserInfo(cursor, userID):
    return executeSQL(cursor, "select [фамилия], [имя], [отчество], [дата_рождения], [возраст]"
    "from [Работник]"
    "where [id_работника] = '{}'".format(userID))

def getUserContactInfo(cursor, userID):
    return executeSQL(cursor, "select [mail], [номер_телефона]"
    "from [Контактная_информация]"
    "where [id_работника] = '{}'".format(userID))

def getUserPassportInfo(cursor, userID):
    return executeSQL(cursor, "select [серия], [номер], [кем_выдан]"
    "from [Паспортные_данные]"
    "where [id_работника] = '{}'".format(userID))

def getDiskInfo(cursor, userID):
    return executeSQL(cursor, "select [серия], [номер], [кем_выдан]"
    "from [Паспортные_данные]"
    "where [id_работника] = '{}'".format(userID))

def getAllSales(cursor):
    return executeSQLAll(cursor, "select *"
    "from [Покупка]")

def getAllEmployees(cursor):
    return executeSQLAll(cursor, "select *"
    "from [Работник]")

def getAllDisks(cursor):
    return executeSQLAll(cursor, "select *"
    "from [Диск]")

def getAllBuildings(cursor):
    return executeSQLAll(cursor, "select *"
    "from [Филиал]")

def getAllLogins(cursor):
    return executeSQLAll(cursor, "select [логин]"
    "from [Работник_Логин]")

def getAllCustomerCards(cursor):
    return executeSQLAll(cursor, "select *"
    "from [Карта_покупателя]")

def getAllCustomers(cursor):
    return executeSQLAll(cursor, "select *"
    "from [Покупатель]")

def getLastUserId(cursor):
    return executeSQL(cursor, "select max([id_работника])"
    "from [Работник]")

def addEmployee(cursor, values):
    newUserId = int(getLastUserId(cursor)[0]) + 1
    result = list(map(lambda i:''.join(i[0].split()), getAllLogins(cursor)))

    if values[4] in result:
        return 'error'
    return (newUserId, executeSQLUpdate(cursor, "insert into [dbo].[Работник] ([id_работника], [фамилия], [имя], [отчество], [дата_рождения])" +
    "values ({}, '{}', '{}', '{}', '{}')".format(newUserId, values[0], values[1], values[2], values[3]) +
    "insert into [dbo].[Работник_Логин] ([id_работника], [логин], [пароль])" +
    "values ({}, '{}', '{}')".format(newUserId, values[4], values[5])))
