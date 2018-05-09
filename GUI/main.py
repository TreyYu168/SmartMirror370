# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.


from tkinter import *
from pyowm import OWM
from PIL import Image, ImageTk
import io
import time
from urllib.request import urlopen
import face_recognition
import subprocess
import feedparser

class App():
	

	def __init__(self):
		API_key ='77a19323c1f5772016293f6b30b52d15'
		self.owm = OWM(API_key)

		self.root = Tk()

		self.root.configure(background = "black")
		self.root.bind("<Key>", self.key)
		
		self.mainScreen()

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

		self.update_clock()


	def rightScreen(self):


		self.timeLabel = Label(text = "", bg = "black", fg = "white", font=("Comic Sans", 60))
		self.timeLabel.grid(row=0, column=0)

		self.quoteLabel = Label(text = "Right Screen", bg = "black", fg = "white", font=("Courier", 30))
		self.quoteLabel.grid(row = 1, column = 1)

		self.placeHolder = Label(text = "   ", bg = "black", fg = "white")
		self.placeHolder.grid(row = 0, rowspan = 2, column = 2, columnspan = 2, sticky = E)

		self.update_clock()



	def leftScreen(self):


		self.timeLabel = Label(text = "", bg = "black", fg = "white", font=("Comic Sans", 60))
		self.timeLabel.grid(row=0, column=0)

		self.news = self.getNewsArticle()

		self.quoteLabel = Label(text = "News Feed", bg = "black", fg = "white", font=("Courier", 45))
		self.quoteLabel.grid(row = 1, column = 1, sticky = W)

		currRow = 2
		for i in range(0, len(self.news)):
			titleLabel = Label(text = self.news[i][0], bg = "black", fg = "white", font=("Courier", 25), anchor = W)
			descriptionLabel = Label(text = self.news[i][1], bg = "black", fg = "white", font=("Courier", 14), anchor = W)

			currRow = currRow + 1
			titleLabel.grid(row = currRow, column = 1, sticky = W)
			currRow = currRow + 1
			descriptionLabel.grid(row = currRow, column = 1, sticky = W)

		self.update_clock()


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

	def getNewsArticle(self):
		python_rss_url = "http://rss.cnn.com/rss/cnn_topstories.rss"
		feed = feedparser.parse(python_rss_url)

		seperator = "<"
		numberOfNews = len(feed)
		title = feed["channel"]["title"]
		description = feed["channel"]["description"]

		newsArticle = []

		for i in range(0, numberOfNews):
			articleTitle = feed.entries[i].title
			articleFullSummary = feed.entries[i].summary
			articleSummary = articleFullSummary.split(seperator, 1)[0]
			if articleSummary == "":
				articleSummary = "No Summary Available"
			else: 
				articleSummary = articleFullSummary.split(seperator, 1)[0]
		
			article = [articleTitle, articleSummary]
			newsArticle.append(article)

		return newsArticle

	def key(self, event):
		if event.char == "\uf702":
			for label in self.root.winfo_children(): label.destroy()
			self.leftScreen()
		elif event.char == "\uf703":
			for label in self.root.winfo_children(): label.destroy()
			self.rightScreen()
		else:
			for label in self.root.winfo_children(): label.destroy()
			self.mainScreen()

app = App()
