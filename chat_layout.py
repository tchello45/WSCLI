import PySimpleGUI as sg
def chat():
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
chat()