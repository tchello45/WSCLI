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

def login():
    sio.emit('login', {'username': 'test', 'password': 'test', 'API_server': 'sys_default_enc', 'login_password': 123})

def register():
    sio.emit('register', {'username': 'test', 'password': 'test', 'API_server': 'sys', 'register_password': "123"})

sio.connect('http://localhost:5000')
register()
sio.wait()