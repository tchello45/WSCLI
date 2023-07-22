import PySimpleGUI as sg
import os
import json
import shutil
import socketio
sio = socketio.Client()
window = None
enc = None
server_link = None
api_server_name = None
login_password = None
register_password = None
@sio.on('status')
def status(data):
    if data["succes"]:
        if data["code"] == 211 and data["flag"] == "check":
            print("passwords are correct")
            dict_ = {
                "server_link": server_link,
                "api_server_name": api_server_name,
                "login_password": login_password,
                "register_password": register_password,
                "enc": enc
            }
            with open('temp/config.json', 'w') as f:
                json.dump(dict_, f)
            sg.popup_ok('Installation is complete!')

    else:
        if data["code"] == 402 and data["flag"] == "check":
            sg.popup_error('Login password is incorrect')
        if data["code"] == 403 and data["flag"] == "check":
            sg.popup_error('Register password is incorrect')

@sio.on('enc')
def enc(data):
    global enc
    enc = data
    window.close()
def start():
    layout = [
        [sg.Text('Installation', font=('Helvetica', 20))],
        [sg.Text('Server Link'), sg.InputText(key='server_link')],
        [sg.Text('API Server Name'), sg.InputText(key='api_server_name')],
        [sg.Text('Login password'), sg.InputText(key='login_password')],
        [sg.Text('Register password'), sg.InputText(key='register_password')],
        [sg.Button('Next')]
    ]
    global window
    window = sg.Window('Installation', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Next':
            global server_link
            global api_server_name
            global login_password
            global register_password
            server_link = values['server_link']
            api_server_name = values['api_server_name']
            login_password = values['login_password']
            register_password = values['register_password']
            if server_link == '' or api_server_name == '' or login_password == '' or register_password == '':
                sg.popup_error('Please fill in all fields')

            else:
                try:
                    sio.connect(server_link)
                    sio.emit('get_enc_API_server', {'API_server': api_server_name})
                    sio.emit('login_register_password_check', {'login_password': login_password, 'register_password': register_password, 'API_server': api_server_name})
                except:
                    sg.popup_error('Server is offline')
                break
start()