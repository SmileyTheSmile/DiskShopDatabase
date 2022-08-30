import PySimpleGUI as sg
import sql_commands as sc

def loginWindow():
    layout = [[sg.Text('Логин:',  size = (6, 1)), sg.InputText(default_text = 'kdanil01')],
              [sg.Text('Пароль:', size = (6, 1)), sg.InputText(default_text = 'begemot')],
              [sg.Button('Войти'), sg.Button('Выход'), sg.Button('Регистрация')]]
    
    return sg.Window('Войти в систему', layout)

def registerWindow():
    layout = [[sg.Text('Фамилия:', size = (16, 1)), sg.InputText(default_text = 'Васильев')],
              [sg.Text('Имя:',  size = (16, 1)), sg.InputText(default_text = 'Иван')],
              [sg.Text('Отчество:',  size = (16, 1)), sg.InputText(default_text = 'Васильевич')],
              [sg.Text('Дата рождения:',  size = (16, 1)), sg.InputText(default_text = '02-05-1999')],
              [sg.Text('Введите логин:',  size = (16, 1)), sg.InputText(default_text = 'vasya')],
              [sg.Text('Введите пароль:', size = (16, 1)), sg.InputText(default_text = 'vasya')],
              [sg.Text('Подтвердите пароль:', size = (16, 1)), sg.InputText(default_text = 'vasya')],
              [sg.Button('Зарегистрироваться'), sg.Button('Назад'), sg.Button('Выход')]]
    
    return sg.Window('Войти в систему', layout)

def userWindow(cursor, userID, headings, data, tooltip):
    userInfo = sc.getUserInfo(cursor, userID)                 #([фамилия], [имя], [отчество], [дата_рождения], [возраст])
    userPassportInfo = sc.getUserPassportInfo(cursor, userID) #([серия], [номер], [кем_выдан])
    userContactInfo = sc.getUserContactInfo(cursor, userID)   #([mail], [номер_телефона])
    
    data = list(map(lambda i:list(i), data))

    layout = [[sg.Text('{} {} {}, {} ({} лет)'.format(userInfo[0], userInfo[1], userInfo[2], userInfo[3], userInfo[4]), justification='center'), sg.Button('Выйти')],
              [sg.Button('Покупки'), sg.Button('Рабочие'), sg.Button('Диски'), sg.Button('Филиалы'), sg.Button('Карты покупателей'), sg.Button('Покупатели')],
              #[sg.Text('Поиск диска', justification='center'), sg.InputText()],
              [sg.Table(values=data,
                        visible=True,
                        headings=headings,
                        max_col_width=35,
                        background_color='white',
                        auto_size_columns=True,
                        text_color='black',
                        display_row_numbers=False,
                        justification='right',
                        num_rows=len(data),
                        alternating_row_color='lightgray',
                        key='_Table_',
                        row_height=20,
                        tooltip=tooltip)]]
    
    return sg.Window('Окно пользователя', layout, size=(854, 480), element_justification='c')
