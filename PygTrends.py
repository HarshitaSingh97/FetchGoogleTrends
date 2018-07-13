from pytrends.request import TrendReq
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd, requests
class fetchtrends:
        latlng="0,0"
        def __init__(self,keywords,latitude=None,longitude=None,time=None):
                self.keywords = keywords#['asthma','air']
                if time is None:
                        now = datetime.now()
                        three_yrs_ago = now - relativedelta(years=3)
                        default = three_yrs_ago.strftime("%Y-%m-%d") + " " + now.strftime("%Y-%m-%d")
                        self.time = default
                else:
                     	self.time = time
                if latitude is None:
                        self.latitude = "0"
                else :
                      	self.latitude = latitude
                if longitude is None:
                        self.longitude = "0"
                else :
                      	self.longitude = longitude
                self.latlng=self.latitude+","+self.longitude

       	#retreive address of given latitude and longitude. InputFormat: 'latitude,longitude' OutputFormat:JSON
        def reverse_geocode(self,latlng):
                result = {}
                print(latlng)
                url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={}'
                request = url.format(latlng)

                # handling empty response
                while(1):
                        data = requests.get(request).json()
                        if len(data['results']) > 0:
                                result = data['results'][0]
                                break
                return result

       	#Parse 'result' to retrieve Country
        def parse_country(self,geocode_data):
                if (not geocode_data is None) and ('address_components' in geocode_data):
                        for component in geocode_data['address_components']:
                                if 'country' in component['types']:
                                        return component['short_name']
                return None

       	#Parse 'result' to retrieve City
        def parse_city(self,geocode_data):
                if (not geocode_data is None) and ('address_components' in geocode_data):
                        for component in geocode_data['address_components']:
                                #if 'location' in component['types']:
                                        #return component['short_name']
                                #elif 'postal_town' in component['types']:
                                        #return component['short_name']
                                #elif 'administrative_area_level_2' in component['types']:
                                if 'administrative_area_level_1' in component['types']:
                                        return component['short_name']
                return None

        def fetch(self):
                gtgeo=self.reverse_geocode(self.latlng)
                city=self.parse_city(gtgeo)
                country=self.parse_country(gtgeo)
                if(len(city)==2 and len(country)==2):
                        gtcode=country + "-" + city
                elif(len(city)!=2 and len(country)==2):
                        gtcode=country
                else:
                     	gtcode=""
                pytrends = TrendReq(hl='en-US', tz=360)
                pytrends.build_payload(self.keywords, cat=0, timeframe=self.time, geo=gtcode, gprop='')
                return pytrends.interest_over_time()





'''
from pytrends.request import TrendReq
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd, requests
class fetchtrends:
	latlng="0,0"
	def __init__(self,keywords,latitude=None,longitude=None,time=None):
		self.keywords = keywords#['asthma','air']
		if time is None:
			now = datetime.now()
			three_yrs_ago = now - relativedelta(years=3)
			default = three_yrs_ago.strftime("%Y-%m-%d") + " " + now.strftime("%Y-%m-%d")
			self.time = default
		else:
			self.time = time
		if latitude is None:
			self.latitude = "0"
		else :
			self.latitude = latitude
		if longitude is None:
			self.longitude = "0"
		else :
			self.longitude = longitude
		self.latlng=self.latitude+","+self.longitude

	#retreive address of given latitude and longitude. InputFormat: 'latitude,longitude' OutputFormat:JSON
	def reverse_geocode(self,latlng):
		result = {}
		print(latlng)
		url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={}'
		request = url.format(latlng)

		# handling empty response
		while(1):
			data = requests.get(request).json()
			if len(data['results']) > 0:
				result = data['results'][0]
				break
		return result

	#Parse 'result' to retrieve Country
	def parse_country(self,geocode_data):
		if (not geocode_data is None) and ('address_components' in geocode_data):
			for component in geocode_data['address_components']:
				if 'country' in component['types']:
					return component['short_name']
		return None

	#Parse 'result' to retrieve City
	def parse_city(self,geocode_data):
		if (not geocode_data is None) and ('address_components' in geocode_data):
			for component in geocode_data['address_components']:
				#if 'location' in component['types']:
					#return component['short_name']
				#elif 'postal_town' in component['types']:
					#return component['short_name']
				#elif 'administrative_area_level_2' in component['types']:
					#return component['short_name']
				if 'administrative_area_level_1' in component['types']:
					return component['short_name']
		return None

	def fetch(self):
		gtgeo=self.reverse_geocode(self.latlng)
		city=self.parse_city(gtgeo)
		country=self.parse_country(gtgeo)
		if(len(city)==2 and len(country)==2):
			gtcode=country + "-" + city
		elif(len(city)!=2 and len(country)==2):
			gtcode=country
		else:
			gtcode=""
		pytrends = TrendReq(hl='en-US', tz=360)
		pytrends.build_payload(self.keywords, cat=0, timeframe=self.time, geo=gtcode, gprop='')
		return pytrends.interest_over_time()
'''
