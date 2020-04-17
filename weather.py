
import requests
import json
import datetime

def weather():
	url_weather = "https://api.weather.com/v3/wx/forecast/daily/5day?geocode=48.92,2.21&format=json&units=m&language=fr-FR&apiKey=205254c6102c4a789254c6102c7a78d0"
	r_weather = requests.get(url_weather)
	data = r_weather.json()

	daypartName = data['daypart'][0]['daypartName'][1]
	narrative = data['daypart'][0]['narrative'][1]
	precipchance = data['daypart'][0]['precipChance'][1]
	temperature = data['daypart'][0]['temperature'][1]
	if precipchance < 60:
		print("Arrosage recommandé")
	print("{} : {} °C - {} %".format(daypartName, temperature, precipchance))

def weather_forcast():

	url_weather = "https://api.weather.com/v3/wx/forecast/daily/5day?geocode=48.92,2.21&format=json&units=m&language=fr-FR&apiKey=205254c6102c4a789254c6102c7a78d0"
	r_weather = requests.get(url_weather)
	data = r_weather.json()

	for i in range (0,11):
		daypartName = data['daypart'][0]['daypartName'][i]
		narrative = data['daypart'][0]['narrative'][i]
		precipchance = data['daypart'][0]['precipChance'][i]
		temperature = data['daypart'][0]['temperature'][i]
		print("{} : {} °C - {} %".format(daypartName, temperature, precipchance))
		