import PySimpleGUI as sg
import json
import socketio
import os
sio = socketio.Client()
path = None
window = None
enc = None
server_adress = None
api_server_name = None
login_password = None
register_password = None
def main():
    layout = [
        [sg.Text('WSCLI', font=('Helvetica', 20))],
        [sg.Button('Open Config'), sg.Button('Create Config'), sg.Button('One Time Usage')],
        [sg.Button('Exit')]
    ]
    window = sg.Window('WSCLI', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Open Config':
            window.close()
            open_config()
            break
        if event == 'Create Config':
            window.close()
            create_config()
            break
        if event == 'One Time Usage':
            pass
def open_config():
    global server_adress
    global api_server_name
    global login_password
    global register_password
    global path   
    global enc     
    layout = [
        [sg.Text('Open Config', font=('Helvetica', 20))],
        [sg.InputText(key='path'), sg.FileBrowse('Select path', file_types=(('wscli config', '*.wscli'),))],
        [sg.Button('Next')]
    ]
    window = sg.Window('WSCLI', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Next':
            path = values['path']
            if path == '':
                sg.popup_error('Path is empty')
                continue
            if not os.path.exists(path):
                sg.popup_error('Path does not exist')
                continue
            try:
                data = json.loads(open(path, "r").read())
                server_adress = data["server_link"]
                api_server_name = data["api_server_name"]
                login_password = data["login_password"]
                register_password = data["register_password"]
                enc = data["enc"]
            except:
                sg.popup_error('Config is invalid')
                continue

            break
    window.close()
def create_config():
    global server_adress
    global api_server_name
    global login_password
    global register_password
    global path
    layout = [
        [sg.Text('Create Config', font=('Helvetica', 20))],
        [sg.InputText(key='path'), sg.FileSaveAs('Select path', file_types=(('wscli config', '*.wscli'),))],
        [sg.Text('Server Adress'), sg.InputText(key='server_adress')],
        [sg.Text('API Server Name'), sg.InputText(key='api_server_name')],
        [sg.Text('Login Password'), sg.InputText(key='login_password', password_char='*')],
        [sg.Text('Register Password'), sg.InputText(key='register_password', password_char='*')],
        [sg.Button('Next'), sg.Button('Finish (Create User later)')]
    ]
    window = sg.Window('WSCLI', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Next':
            path = values['path']
            server_adress = values['server_adress']
            api_server_name = values['api_server_name']
            login_password = values['login_password']
            register_password = values['register_password']
            if path == '' or server_adress == '' or api_server_name == '' or login_password == '' or register_password == '':
                sg.popup_error('Please fill in all fields')
            else:
                try:
                    sio.connect(server_adress)
                    sio.emit('get_enc_API_server', {'API_server': api_server_name})
                    sio.emit('login_register_password_check', {'login_password': login_password, 'register_password': register_password, 'API_server': api_server_name})
                except:
                    sg.popup_error('Server is offline')
                    continue
                break
        if event == 'Finish (Create User later)':
            path = values['path']
            server_adress = values['server_adress']
            api_server_name = values['api_server_name']
            login_password = values['login_password']
            register_password = values['register_password']
            if path == '' or server_adress == '' or api_server_name == '' or login_password == '' or register_password == '':
                sg.popup_error('Please fill in all fields')
            else:
                try:
                    sio.connect(server_adress)
                    sio.emit('get_enc_API_server', {'API_server': api_server_name})
                    sio.emit('login_register_password_check', {'login_password': login_password, 'register_password': register_password, 'API_server': api_server_name})
                except:
                    sg.popup_error('Server is offline')
                    continue
                break
    window.close()
def one_time_usage():
    layout = [
        [sg.Text('One Time Usage', font=('Helvetica', 20))],
        [sg.Text('Server Adress'), sg.InputText(key='server_adress')],
        [sg.Text('API Server Name'), sg.InputText(key='api_server_name')],
        [sg.Text('Login Password'), sg.InputText(key='login_password', password_char='*')],
        [sg.Text('Register Password'), sg.InputText(key='register_password', password_char='*')],
        [sg.Button('Next')]
    ]
    window = sg.Window('WSCLI', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Next':
            server_adress = values['server_adress']
            api_server_name = values['api_server_name']
            login_password = values['login_password']
            register_password = values['register_password']
            if server_adress == '' or api_server_name == '' or login_password == '' or register_password == '':
                sg.popup_error('Please fill in all fields')
            else:
                try:
                    sio.connect(server_adress)
                    sio.emit('get_enc_API_server', {'API_server': api_server_name})
                    sio.emit('login_register_password_check', {'login_password': login_password, 'register_password': register_password, 'API_server': api_server_name})
                except:
                    sg.popup_error('Server is offline')
                    continue
                break
def user():
    layout = [
        [sg.Text('Login/SignUp', font=('Helvetica', 20))],
        [sg.Text('Username'), sg.InputText(key='username')],
        [sg.Text('Password'), sg.InputText(key='password', password_char='*')],
        [sg.Button('Login'), sg.Button('SignUp')]
    ]
    window = sg.Window('WSCLI', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Login':
            username = values['username']
            password = values['password']
            if username == '' or password == '':
                sg.popup_error('Please fill in all fields')
            else:
                pass
        if event == 'SignUp':
            username = values['username']
            password = values['password']
            if username == '' or password == '':
                sg.popup_error('Please fill in all fields')
            else:
                pass
@sio.on('status')
def status(data):
    if data["succes"]:
        if data["code"] == 211 and data["flag"] == "check":
            print("passwords are correct")
            dict_ = {
                "server_link": server_adress,
                "api_server_name": api_server_name,
                "login_password": login_password,
                "register_password": register_password,
                "enc": enc
            }
            json_ = json.dumps(dict_)
            da = open(path, "w")
            da.write(json_)
            da.close()
    else:
        if data["code"] == 402 and data["flag"] == "check":
            print("login password is incorrect")
        if data["code"] == 403 and data["flag"] == "check":
            print("register password is incorrect")
@sio.on('enc')
def enc_(data):
    global enc
    enc = data
main()
print(f"""
{server_adress}
{api_server_name}
{login_password}
{register_password}
{path}
{enc}
      """)