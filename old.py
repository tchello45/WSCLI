import socketio

sio = socketio.Client()
@sio.event
def connect():
    print('Connected to server')

@sio.event
def disconnect():
    print('Disconnected from server')
    sio.disconnect()

@sio.on('status')
def status(data):
    print(data)

@sio.on('token')
def token(data):
    token_ = data
    da = open('temp/token.txt', 'w')
    da.write(data)
    da.close()

def login():
    sio.emit('login', {'username': 'test', 'password': 'test', 'API_server': 'sys', 'login_password': "123"})

def register():
    sio.emit('register', {'username': 'test', 'password': 'test', 'API_server': 'sys', 'register_password': "123"})

def token_check():
    da = open('token.txt', 'r')
    token = da.read()
    da.close()
    sio.emit('token_check', {'token': token})
    sio.emit('token_check', {'token': "token"})

sio.connect('http://localhost:5000')
token_check()
sio.wait()