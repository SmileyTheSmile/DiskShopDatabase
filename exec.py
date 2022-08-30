import pyodbc 
import PySimpleGUI as sg

import user_windows as uw
import sql_commands as sc

def loginLoop(cursor):
    current_window = uw.loginWindow()
    
    while True:
        event, values = current_window.read()
        
        if event == sg.WIN_CLOSED or event == 'Выход':
            current_window.close()  
            return 'quit'
        
        elif event == 'Войти':
            userID = sc.getUserID(cursor, values)

            if userID == None:
                sg.popup_ok('Неправильный логин или пароль.')  
            elif userID == 'error':
                sg.popup_ok('Ошибка запроса к базе данных.')  
            else:
                current_window.close()  
                return 'workWindow' + str(userID[0])
                
        if event == 'Регистрация': 
            current_window.close() 
            return 'registrationWindow'

def registrationLoop(cursor):
    current_window = uw.registerWindow()
    
    while True:
        event, values = current_window.read()

        if event == sg.WIN_CLOSED or event == 'Выход':
            current_window.close()  
            return 'quit'
        
        elif event == 'Зарегистрироваться': 
            if values[5] == values[6]:
                result = sc.addEmployee(cursor, values)

                if result == 'error':
                    sg.popup_ok('Логин уже занят')  
                else:
                    current_window.close()  
                    return 'workWindow' + str(result[0])
            else:
                sg.popup_ok('Пароли не совпадают') 
                        
        elif event == 'Назад': 
            current_window.close() 
            return 'loginWindow'

def workWindowLoop(cursor, userID):
    current_window = uw.userWindow(cursor, 
                                        userID, 
                                        ['id_покупателя', 'id_диска', 'id_филиала', 'id_карты_скидок', 'id_работника', 'дата_покупки'],
                                        sc.getAllSales(cursor),
                                        'Рабочие')
    
    while True:
        event, values = current_window.read()

        if event == sg.WIN_CLOSED:
            current_window.close()  
            return 'quit'
        
        elif event == 'Покупки': 
            current_window.close()  
            current_window = uw.userWindow(cursor, 
                                            userID, 
                                            ['id_покупателя', 'id_диска', 'id_филиала', 'id_карты_скидок', 'id_работника', 'дата_покупки'],
                                            sc.getAllSales(cursor),
                                            'Рабочие')

        elif event == 'Рабочие': 
            current_window.close()  
            current_window = uw.userWindow(cursor, 
                                            userID, 
                                            ['id_работника', 'фамилия', 'имя', 'отчество', 'дата_рождения', 'возраст'],
                                            sc.getAllEmployees(cursor),
                                            'Рабочие')
        
        elif event == 'Диски': 
            current_window.close()  
            current_window = uw.userWindow(cursor, 
                                            userID, 
                                            ['id_диска', 'тип', 'цена'],
                                            sc.getAllDisks(cursor),
                                            'Диски')
            
        elif event == 'Филиалы': 
            current_window.close()  
            current_window = uw.userWindow(cursor, 
                                            userID, 
                                            ['id_филиала', 'адрес', 'рейтинг', 'количество_работников'],
                                            sc.getAllBuildings(cursor),
                                            'Филиалы')
            
        elif event == 'Карты покупателей': 
            current_window.close()  
            current_window = uw.userWindow(cursor, 
                                            userID, 
                                            ['id_карты', 'id_покупателя', 'дата_выдачи', 'активна_до', 'период_активности'],
                                            sc.getAllCustomerCards(cursor),
                                            'Филиалы')
            
        elif event == 'Покупатели': 
            current_window.close()  
            current_window = uw.userWindow(cursor, 
                                            userID, 
                                            ['id_покупателя', 'фамилия', 'имя', 'отчество', 'номер_телефона', 'есть_ли_карта'],
                                            sc.getAllCustomers(cursor),
                                            'Покупатели')
                        
        elif event == 'Выйти': 
            current_window.close() 
            return 'loginWindow'
    
def execute():
    sg.theme('DarkAmber')
    cursor = sc.connectToSQL()
    
    result = loginLoop(cursor)
    
    while True:
        if result == 'loginWindow':
            result = loginLoop(cursor)        
        if result == 'registrationWindow':
            result = registrationLoop(cursor)
        elif result[:10] == 'workWindow':
            result = workWindowLoop(cursor, result[10:])
        elif result == 'quit':
            break
    
execute()  