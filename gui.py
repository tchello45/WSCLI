import PySimpleGUI as sg
import threading

def start():
    sg.popup_ok('Installation is complete!')

threading.Thread(target=start).start()