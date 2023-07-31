import PySimpleGUI as sg
import os
import json
import socketio
import rsa
import threading
import zipper
sio = socketio.Client()
window = None
token_ = None
target_ = None
__version__ = "1.0.0 beta"
__author__ = "Tilman Kurmayer"
layout = [
    [sg.Text(f'WSCLI {__version__}', font=('Helvetica', 20))],
    [sg.InputText(key="path"), sg.FileBrowse('Select config', file_types=(('wscli config', '*.wscli'),))],
    [sg.Button('Start')]
]
window = sg.Window('WSCLI', layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Start':
        path = values['path']
        break
window.close()
window = None
if path == '':
    sg.popup_error('Path is empty')
    exit()
if not os.path.exists(path):
    sg.popup_error('Path does not exist')
    exit()
try:
    data = json.loads(zipper.read_config(path).decode())
except:
    sg.popup_error('Config is invalid')
    exit()
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
def web_sock_messages_background(target:str):

    print("start backgorund"+ target)
    sio.emit('get_messages_background', {'target': target, 'token': token_})

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
            chat()
    

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
            login()

def chat():
    global window
    global target_
    layout = [
        [sg.Text('Chat', font=('Helvetica', 20), key="title")],
        [sg.Text('Messages', font=('Helvetica', 15))],
        [sg.Multiline(key='messages', size=(1000, 25), disabled=True)],
        [sg.Text('Target'), sg.InputText(key='target'), sg.Button('Set')],
        [sg.Text('Message'), sg.InputText(key='message')],
        [sg.Button('Send'), sg.Button('Load'), sg.Button('Logout')]
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
            target_ = target
        if event == 'Load':
            target = values['target']
            if target == '':
                sg.popup_error('Target is empty')
                continue
            target_ = target
            threading.Thread(target=web_sock_get_messages, args=(target,)).start()    
        if event == 'Set':
            target = values['target']
            if target == '':
                sg.popup_error('Target is empty')
                continue
            target_ = target
            window["title"].update(f"Chat with {target}")
            threading.Thread(target=web_sock_get_messages, args=(target,)).start() 
            threading.Thread(target=web_sock_messages_background, args=(target,)).start()
        if event == 'Logout':
            global token_
            token_ = None
            zipper.save_token('conf.wscli', "INVALID_TOKEN")
            window.close()
            register_login()
            break

@sio.on('status')
def status(data):
    zipper.save_long_log('conf.wscli', str(data))
    zipper.save_log('conf.wscli', str(data["err_id"]))
    if data["code"] == 401 and data["flag"] == "check":
        register_login()
    elif data["code"] == 210 and data["flag"] == "check":
        chat()
    if data["code"] == 410 and data["flag"] == "get_messages":
        window['messages'].update('Target not found')
@sio.on('error_dict')
def error_dict(data):
    zipper.save_error_dict('conf.wscli', data)
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
    zipper.save_token('conf.wscli', token_)
    print(token_)
@sio.on('messages_background')
def messages_background(data):
    new_data = ''
    for i in data:
        new_data += f"{i['sender']} at {i['timestamp']}: '{i['message'].decode()}'\n"
    old_data = window['messages'].get()
    window['messages'].update(old_data + "\n" + new_data)
    global target_
    threading.Thread(target=web_sock_messages_background, args=(target_,)).start()


try:
    sio.connect(server_link)
except: 
    sg.popup_error('Server is not available')
    exit()

try:
    token_ = zipper.read_token(path).decode()
    web_sock_check_token(token_)
except Exception as e:
    register_login()
exit()
