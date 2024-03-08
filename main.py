import PySimpleGUI as sg
import re
import random
from cryptography.fernet import Fernet

# changing the appearance/color scheme of the window
sg.theme('Dark2')

# this layout represents what is going inside the window
layout = [
    [sg.Image(r'header.png')],
    [sg.Text('')],
    [sg.Text('Please type in your first and last name here (This will be your username. Spaces will be removed):',text_color='cyan')],
    [sg.InputText('', key='input_name', size=(30,1))],
    [sg.Text('Please input your password here (Spaces will be removed):', text_color='cyan')],
    [sg.InputText('', password_char='*', key='input_passwd', size=(30, 1))], #password_char changes the physical appearance of the text and hides what the user is putting in. The key saves the input to a variable
    [sg.Button('Check', bind_return_key=True), sg.Button("Generate Password"), sg.Button("Close")],
    [sg.FileBrowse('Import .txt File (DO THIS 1ST IF IMPORTING FILE)', key='in', file_types=(("Text Files", "*.txt"),)), sg.Button('Check .txt File (DO THIS 2ND)')],
    [sg.Text("From a scale of 0-7 (0 the best 7 the worst), the security of the last attempted password is a:", text_color='cyan'), sg.Listbox(values=(' '), size=(7, 1), key='scale')],
    [sg.Text("Password is strong? Encrypt it here! ",text_color='cyan'), sg.InputText('', password_char='*', key='enc',size=(30,1)), sg.Button('Encrypt it!')]
]

# Creating the window. This changes the name of the program, adding out layout list, and making the window resizable
window = sg.Window('Password Checker', layout, default_element_size=(12, 1), resizable=True, finalize=True, icon='logo.ico')

#variable definitions used throughout the program
passwd1 = None
passwd2 = None
passwd3 = None
passwd4 = None
lowercase = re.compile("(?=(.*[a-z]){2,})")
uppercase = re.compile("(?=(.*[A-Z]){2,})")
digits = re.compile("(?=(.*[0-9]){2,})")
special = re.compile("(?=(.*[@#$&*]){2,})")
count = 0
v1 = 0
v2 = 0
v3 = 0
v4 = 0
v5 = 0
v6 = 0
v7 = 0

# event loop if the window running constantly
while True:
    event, values, = window.read()

    if event == sg.WIN_CLOSED or event == 'Close':  # If user closes window or clicks cancel
        break

    if event == 'Check':
        passwd = str(values['input_passwd']) # assigns the input to a variable to check the password
        name = str(values['input_name']) # assigns the input to a variable to check the username
        passwd = passwd.replace(' ', '') # This line and the line below will remove any spaces the user inputs to keep consistency
        name = name.replace(' ', '')
        if len(passwd) <= 14: #character limit
            sg.popup(passwd,"is an invalid password. Less than 14 characters")
            count = 1
            v1 = 1
        if not lowercase.match(passwd): #lowercase checker
            sg.popup(passwd,"is an invalid password. Less than 2 lowercase characters")
            count = 1
            v2 = 1
        if not uppercase.match(passwd): #uppercase checker
            sg.popup(passwd,"is an invalid password. Less than 2 uppercase characters")
            count = 1
            v3 = 1
        if not digits.match(passwd): #digit checker
            sg.popup(passwd,"is an invalid password. Less than 2 digits")
            count = 1
            v4 = 1
        if not special.match(passwd): #special character checker
            sg.popup(passwd,"is an invalid password. Less than 2 special characters")
            count = 1
            v5 = 1
        if bool(re.search(name,passwd)) == True: #username checker
            sg.popup(passwd, "is an invalid password. Cannot be your username")
            count = 1
            v6 = 1
        if passwd == passwd1 or passwd == passwd2 or passwd == passwd3 or passwd == passwd4: #memory checker
            sg.popup(passwd, "is an invalid password. Cannot be previously used")
            count = 1
            v7 = 1
        if count == 0:
            sg.popup("Valid password:", passwd)
        v8 = v1 + v2 + v3 + v4 + v5 + v6 + v7
        if passwd1 == None: #these lines below passes the password that was just inputed through a line of varibales to store in memory
            passwd1 = passwd
        if passwd2 == None:
            passwd2 = passwd1
        if passwd3 == None:
            passwd3 = passwd2
        if passwd4 == None:
            passwd4 = passwd3
        window.Element('scale').update(values=[v8]) #prints out this number in the box to tell the user how strong the password is
        count = 0

    #password generator
    if event == "Generate Password":
        result_passwd = ''.join((random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(5)))
        result_passwd2 = ''.join((random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(5)))
        result_passwd3 = ''.join((random.choice('0123456789') for i in range(5)))
        result_passwd4 = ''.join((random.choice('@#$&*') for i in range(3)))
        result_passwdpre = result_passwd + result_passwd2 + result_passwd3 + result_passwd4
        result_passwdfinal = ''.join(random.sample(result_passwdpre,len(result_passwdpre)))
        sg.popup("Your password is:", result_passwdfinal)

    if event == 'Check .txt File (DO THIS 2ND)':
        count = 0
        #this following code below is how the program starts to read the program and identifies each word that is listed in the text file. After that, it checks like it did above.
        with open(values['in']) as f:
            lines = f.read().replace('\n', '')
        with open(values['in']) as f:
            text_dump = f.read()
        text_dump = text_dump.replace(" ", "")
        list_of_passwds = text_dump.split(",")
        print(list_of_passwds)
        sg.popup("Your password(s) is:", list_of_passwds)
        name = str(values['input_name'])  # assigns the input to a variable to check the username
        name = name.replace(' ', '')
        for lines in list_of_passwds:
            if len(lines) <= 14:  # character limit
                sg.popup(lines, "is an invalid password. Less than 14 characters")
                count = 1
                v1 = 1
            if not lowercase.match(lines):
                sg.popup(lines, "is an invalid password. Less than 2 lowercase characters")
                count = 1
                v2 = 1
            if not uppercase.match(lines):
                sg.popup(lines, "is an invalid password. Less than 2 uppercase characters")
                count = 1
                v3 = 1
            if not digits.match(lines):
                sg.popup(lines, "is an invalid password. Less than 2 digits")
                count = 1
                v4 = 1
            if not special.match(lines):
                sg.popup(lines, "is an invalid password. Less than 2 special characters")
                count = 1
                v5 = 1
            if bool(re.search(name,lines)) == True:  # username checker
                sg.popup(lines, "is an invalid password. Cannot be your username")
                count = 1
                v6 = 1
            if lines == passwd1 or lines == passwd2 or lines == passwd3 or lines == passwd4:  # memory checker
                sg.popup(lines, "is an invalid password. Cannot be previously used")
                count = 1
                v7 = 1
            if count == 0:
                sg.popup("Valid password:", lines)
        count = 0

    if event == 'Encrypt it!': #random encryption method
        enc = str(values['enc'])
        print(enc)
        key = Fernet.generate_key()
        fernet = Fernet(key)
        encpass = fernet.encrypt(enc.encode())
        sg.popup("Your password encrypted is: ", encpass)
        decpass = fernet.decrypt(encpass).decode()
        sg.popup("Your password decrypted is: ", decpass)
window.close()
