# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.


from Tkinter import *
from pyowm import OWM
import Image, ImageTk
import time
	
class App():

	
	def set_path(self, str):
		#You still need to figure out the timing of this
		if str == "Clear":
			return "./WeatherIcons/Sunny.png"
		
		if str == "Fog":
			return "./WeatherIcons/Fog.png"
		

		if str == "Haze": 
			return "./WeatherIcons/Haze.png"
		

		if str == "Rain":
			return "./WeatherIcons/HeavyRain.png"
		
		#Again, still need to figure the time
		if str == "Partly Cloudy": 
			return "./WeatherIcons/PartlyCloudy.png"
		
		if str == "Sunny":
			return "./WeatherIcons/Sunny.png"
		
		if str == "Windy":
			return "./WeatherIcons/Windy.png"
		


		
	def __init__(self):

		API_key ='77a19323c1f5772016293f6b30b52d15'
		owm = OWM(API_key)

		obs = owm.weather_at_place('Fort Collins, US')
		loc = obs.get_location()
		w = obs.get_weather()
	
		cityName = loc.get_name()
		curWeather = w.get_status()
		curTemp = w.get_temperature('fahrenheit')['temp']
		
		#######################################################

		
		#######################################################
		self.root = Tk()
		self.root.configure(background = "black")

		self.timeLabel = Label(text = "", bg = "black", fg = "white", font=("Comic Sans", 60))
		self.timeLabel.grid(row=0, column=0)

		self.quoteLabel = Label(text = "Hey Sexy", bg = "black", fg = "white", font=("Courier", 30))
		self.quoteLabel.grid(row = 1, column = 1)
		
		self.tempLabel = Label(text = '%.0f'%(curTemp) + u'\u00B0' + "F",  bg = "black", fg = "white", font=("Comic Sans", 45))
		self.tempLabel.grid(row = 0, column = 2)		
		self.weatherLabel = Label(text = curWeather,  bg = "black", fg = "white", font=("Comic Sans", 45))
		self.weatherLabel.grid(row = 1, column = 2, stick = E)
		
		path = self.set_path(curWeather)

		img = ImageTk.PhotoImage(Image.open(path))
		self.iconLabel = Label(image = img,  bg = "black", fg = "white", font=("Comic Sans", 45))
		self.iconLabel.grid(row = 0, rowspan = 2, column = 3, sticky = E)

		self.root.columnconfigure(1, weight = 3)

		self.update_clock()
		self.root.attributes("-fullscreen", True)
		self.root.mainloop()

	def update_clock(self):
		now = time.strftime("%H:%M")
		self.timeLabel.configure(text = now)
		self.root.after(60000, self.update_clock)

		
app=App()

