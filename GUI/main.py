# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.


from tkinter import *
from pyowm import OWM
from PIL import Image, ImageTk
#import resizeimage
import io
import time
from urllib.request import urlopen
import face_recognition
import subprocess

class App():
	

	def __init__(self):
		API_key ='77a19323c1f5772016293f6b30b52d15'
		self.owm = OWM(API_key)

		self.root = Tk()

		self.root.configure(background = "black")
		self.root.bind("<Key>", self.key)
		
		self.mainScreen()

		self.update_clock()
		#self.update_text()
		self.root.attributes("-fullscreen", True)
		self.root.mainloop()

	def mainScreen(self):

		self.timeLabel = Label(text = "", bg = "black", fg = "white", font=("Comic Sans", 60))
		self.timeLabel.grid(row=0, column=0)

		self.quoteLabel = Label(text = "Hey Sexy", bg = "black", fg = "white", font=("Courier", 30))
		self.quoteLabel.grid(row = 1, column = 1)
		
		self.weatherInfo()
		self.tempLabel = Label(text = '%.0f'%(self.curTemp) + u'\u00B0' + "F",  bg = "black", fg = "white", font=("Comic Sans", 45))
		self.tempLabel.grid(row = 0, column = 2)		
		
		self.weatherLabel = Label(text = self.curWeather,  bg = "black", fg = "white", font=("Comic Sans", 45))
		self.weatherLabel.grid(row = 1, column = 2, stick = E)
		
		img = ImageTk.PhotoImage(self.im)

		self.iconLabel = Label(image = img,  bg = "black", fg = "white", font=("Comic Sans", 45))
		self.iconLabel.grid(row = 0, rowspan = 2, column = 3, sticky = E)

		self.root.columnconfigure(1, weight = 3)

	def rightScreen(self):
		self.quoteLabel.destroy()
		self.tempLabel.destroy()
		self.weatherLabel.destroy()

		self.quoteLabel = Label(text = "Right Screen", bg = "black", fg = "white", font=("Courier", 30))
		self.quoteLabel.grid(row = 1, column = 1)


	def leftScreen(self):
		self.quoteLabel.destroy()
		self.tempLabel.destroy()
		self.weatherLabel.destroy()

		self.quoteLabel = Label(text = "Left Screen", bg = "black", fg = "white", font=("Courier", 30))
		self.quoteLabel.grid(row = 1, column = 1)


	def update_clock(self):
		now = time.strftime("%H:%M")
		self.timeLabel.configure(text = now)
		self.root.after(60000, self.update_clock)

	def update_text(self):
		currentText = "Hello"
		subprocess.call("./capture.sh", shell=True)

		trey_image = face_recognition.load_image_file("Trey_Yu.jpg")
		trey_face_encoding = face_recognition.face_encodings(trey_image)[0]


		jake_image = face_recognition.load_image_file("Jake_Marrapode.jpg")
		jake_face_encoding = face_recognition.face_encodings(jake_image)[0]

		face_locations = []
		face_encodings = []
		image = face_recognition.load_image_file("./CurrentPic/MaybeFace.jpg")

		face_locations = face_recognition.face_locations(image)

		face_encodings = face_recognition.face_encodings(image, face_locations)
		
		for face_encoding in face_encodings:
			treymatch = face_recognition.compare_faces([trey_face_encoding], face_encoding)
			jakematch = face_recognition.compare_faces([jake_face_encoding], face_encoding)

			if treymatch[0]:
				currentText = "Hello Trey"
		
			if jakematch[0]:
				currentText = "Hello Jake"

		self.quoteLabel.configure(text = currentText)
		self.root.after(15000, self.update_text)

	def weatherInfo(self):
		obs = self.owm.weather_at_place('Fort Collins, US')
		loc = obs.get_location()
		w = obs.get_weather()
	
		self.cityName = loc.get_name()
		self.curWeather = w.get_status()
		self.curTemp = w.get_temperature('fahrenheit')['temp']

		url = 'http://openweathermap.org/img/w/' + str(w.get_weather_icon_name()) + '.png'
		raw_data = urlopen(url).read()
		self.im = Image.open(io.BytesIO(raw_data))
		self.im = self.im.resize((150, 150), Image.ANTIALIAS)

	def key(self, event):
		print(repr(event.char))
		if event.char == "\uf702":
			self.leftScreen()
		elif event.char == "\uf703":
			self.rightScreen()
		else:
			self.quoteLabel.destroy()
			self.mainScreen()

app = App()
