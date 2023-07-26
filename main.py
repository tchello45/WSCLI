import PySimpleGUI as sg
import os
import json
import socketio
import rsa
import threading
import sys
from zipfile import ZipFile
sio = socketio.Client()
window = None
token_ = None
if not os.path.exists('temp/config.json'):
    sg.popup_error('Please run installation.py first')
    exit()
with open('temp/config.json', 'r') as f:
    data = json.load(f)
    server_link = data["server_link"]
    api_server_name = data["api_server_name"]
    login_password = data["login_password"]
    register_password = data["register_password"]
    enc = data["enc"]

def web_sock_login(username:str, password:str):
    sio.emit('login', {'username': username, 'password': password, 'API_server': api_server_name, 'login_password': login_password})
def web_sock_register(username:str, password:str, rsa_key_len:int=None):
    if enc:
        print("enc")
        (pubkey, privkey) = rsa.newkeys(rsa_key_len)
        pubkey = pubkey.save_pkcs1()
        privkey = privkey.save_pkcs1()
        sio.emit('register', {'username': username, 'password': password, 'API_server': api_server_name, 'register_password': register_password, 
                              'pub': pubkey.decode('utf8'), 'priv': privkey.decode('utf8')})
    else:
        sio.emit('register', {'username': username, 'password': password, 'API_server': api_server_name, 'register_password': register_password})
def web_sock_send_message(target:str, message:str):
    sio.emit('send_message', {'target': target, 'message': message, 'token': token_})
def web_sock_get_messages(target:str):
    sio.emit('get_messages', {'target': target, 'token': token_})
def web_sock_error_dict():
    sio.emit('get_error_dict')
def web_sock_check_token(token):
    sio.emit('token_check', {'token': token})

def register_login():
    layout = [
        [sg.Button('Login'), sg.Button('Register')]
    ]
    window = sg.Window('Login/Register', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Login':
            login()
            window.close()
            break
        if event == 'Register':
            register()
            window.close()
            break

def login():
    layout = [
        [sg.Text('Login', font=('Helvetica', 20))],
        [sg.Text('Username'), sg.InputText(key='username')],
        [sg.Text('Password'), sg.InputText(key='password')],
        [sg.Button('Login')]
    ]
    window = sg.Window('Login', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Login':
            username = values['username']
            password = values['password']
            threading.Thread(target=web_sock_login, args=(username, password)).start()
            window.close()
            break

def register():
    if enc:
        layout = [
            [sg.Text('Register', font=('Helvetica', 20))],
            [sg.Text('Username'), sg.InputText(key='username')],
            [sg.Text('Password'), sg.InputText(key='password')],
            [sg.Text('RSA Key Length'), sg.DropDown(('512', '1024', '2048', '4096'), default_value='1024', key='rsa_key_len', enable_events=True)],
            [sg.Button('Register')]
        ]
    else:
        layout = [
            [sg.Text('Register', font=('Helvetica', 20))],
            [sg.Text('Username'), sg.InputText(key='username')],
            [sg.Text('Password'), sg.InputText(key='password')],
            [sg.Button('Register')]
        ]
    window = sg.Window('Register', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Register':
            username = values['username']
            password = values['password']
            if enc:
                rsa_key_len = values['rsa_key_len']
                threading.Thread(target=web_sock_register, args=(username, password, int(rsa_key_len))).start()
            else:
                threading.Thread(target=web_sock_register, args=(username, password)).start()
            window.close()
            break

def chat():
    global window
    layout = [
        [sg.Text('Chat', font=('Helvetica', 20))],
        [sg.Text('Messages', font=('Helvetica', 15))],
        [sg.Multiline(key='messages', size=(1000, 25), disabled=True)],
        [sg.Text('Target'), sg.InputText(key='target')],
        [sg.Text('Message'), sg.InputText(key='message')],
        [sg.Button('Send'), sg.Button('Load')]
    ]
    window = sg.Window('Chat', layout, size=(1000, 600), resizable=True)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break   
        if event == 'Send':
            target = values['target']
            message = values['message']
            if target == '' or message == '':
                sg.popup_error('Target or message is empty')
                continue
            threading.Thread(target=web_sock_send_message, args=(target, message)).start()    
            threading.Thread(target=web_sock_get_messages, args=(target,)).start()  
        if event == 'Load':
            target = values['target']
            if target == '':
                sg.popup_error('Target is empty')
                continue
            threading.Thread(target=web_sock_get_messages, args=(target,)).start()     

@sio.on('status')
def status(data):
    da = open('temp/long_log.txt', 'a')
    da.write(str(data) + '\n')
    da.close()
    da = open('temp/log.txt', 'a')
    da.write(str(data["err_id"]) + '\n')
    da.close()
    if data["code"] == 401 and data["flag"] == "check":
        register_login()
    elif data["code"] == 210 and data["flag"] == "check":
        chat()
    if data["code"] == 410 and data["flag"] == "get_messages":
        window['messages'].update('Target not found')
@sio.on('error_dict')
def error_dict(data):
    da = open('temp/error_dict.json', 'w')
    da.write(data)
    da.close()
@sio.on('messages')
def messages(data): 
    new_data = ''
    for i in data:
        new_data += f"{i['sender']} at {i['timestamp']}: '{i['message'].decode()}'\n"
    window['messages'].update(new_data)
@sio.on('token')
def token(data):
    global token_
    token_ = data
    da = open('temp/token.txt', 'w')
    da.write(token_)
    da.close()
    print(token_)
    chat()
try:
    sio.connect(server_link)
except:
    sg.popup_error('Server is not available')
    exit()

if not os.path.exists('temp/token.txt'):
    register_login()
else:
    da = open('temp/token.txt', 'r')
    token_ = da.read()
    da.close()
    web_sock_check_token(token_)
web_sock_error_dict()
exit()
