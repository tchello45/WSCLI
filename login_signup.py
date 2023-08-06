import PySimpleGUI as sg
import json
import socketio
import os
import threading
import rsa
import queue
path = None
token_ = None
sio = socketio.Client()
def gui(q, token):
    layout = [
        [sg.Text('Token: ' + token, font=('Helvetica', 20))],
        [sg.Button('Exit')]
    ]
    window = sg.Window('Token', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            q.put(None)
            break
        if event == 'Exit':
            q.put(None)
            break
    window.close()
def startgui(token):
    q = queue.Queue()
    gui_thread = threading.Thread(target=sg.popup, args=(q, "token: " + token,))
    gui_thread.start()
    
    q.get()

def login_registration():
    global path
    layout = [
        [sg.Text('Login or registration', font=('Helvetica', 20))],
        [sg.InputText(key='path'), sg.FileBrowse('Select path', file_types=(('wscli config', '*.json'),))],
        [sg.Text('Username'), sg.InputText(key='username')],
        [sg.Text('Password'), sg.InputText(key='password')],
        [sg.Button('Login'), sg.Button('SignUp')]
    ]
    window = sg.Window('Login or registration', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Login':
            path = values['path']
            if os.path.exists(path):
                da = open(path, "r")
                data = json.loads(da.read())
                da.close()
                sio.connect(data["server_link"])
                sio.emit('login', {"API_server": data["api_server_name"], "login_password": data["login_password"], "username": values["username"], "password": values["password"]})
            else:
                print("path is incorrect")
            break
        if event == 'SignUp':
            path = values['path']
            if os.path.exists(path):
                da = open(path, "r")
                data = json.loads(da.read())
                da.close()
                sio.connect(data["server_link"])
                if not data["enc"]:
                    sio.emit('register', {"API_server": data["api_server_name"], "register_password": data["register_password"], "username": values["username"], "password": values["password"]})
                else:
                    (pubkey, privkey) = rsa.newkeys(512) 
                    sio.emit('register', {"API_server": data["api_server_name"], "register_password": data["register_password"], "username": values["username"], "password": values["password"], "public_key": pubkey, "private_key": privkey})
            else:
                print("path is incorrect")
            break
    window.close()
@sio.on('status')
def status(data):
    if data["succes"]:
        if data["code"] == 200 and data["flag"] == "login":
            print("login succes")
            exit()
        if data["code"] == 201 and data["flag"] == "register":
            print("register succes")
            exit()
    else:
        if data["code"] == 402 and data["flag"] == "login":
            print("login password is incorrect")
        if data["code"] == 403 and data["flag"] == "register":
            print("register password is incorrect")
        if data["code"] == 420 and data["flag"] == "register":
            print("username is already taken")
    print(data["err_id"])
@sio.on("token")
def token(data):
    global token_
    token_ = data
    da = open("token.json", "w")
    da.write(json.dumps({"token": data}))
    da.close()
login_registration()