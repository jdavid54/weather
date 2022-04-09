import requests
import inspect

from pprint import pprint

from datetime import datetime, timedelta
today = datetime.now()
import datetime as dt

debug = False

# locked with onecall
API_Key = 'edffd1bf975a74d5d10e58c5ac8be2d3'

# my API keys
# API_Key = 'c9d926a9549ae7933324ef26e13bb200'
# API_Key = '56040ff66d50184c81a4df3a770657e3'

#city = input('Enter city name :')
city = 'gagny'
base_url = 'http://api.openweathermap.org/data/2.5/weather?appid='+API_Key+'&q='+city

weather_data = requests.get(base_url).json()

if debug: pprint(weather_data)
if debug: print(weather_data['name'],weather_data['coord'])
if debug: pprint(weather_data['main'])
if debug: print('Temp:',weather_data['main']['temp']-273.15)

lat = weather_data['coord']['lat']
lon = weather_data['coord']['lon']

# onecall : https://openweathermap.org/api/one-call-api
base_url = 'https://api.openweathermap.org/data/2.5/onecall?lat='+str(lat)+'&lon='+str(lon)+'&units=metric&exclude=hourly,minutely&appid='+API_Key
try:
    onecall_data = requests.get(base_url).json()
    # pprint(onecall_data)  # keys : current, lat, lon,minutely,timezone, timezone_offset
    if debug:pprint(onecall_data['current'])
except:
    exit()


# Turns a dictionary into a class
class Dict2Class(object):
    def __init__(self, my_dict):
        
        for key in my_dict:
            if debug: print(key,my_dict[key])
            try:
                setattr(self, key, my_dict[key])
            except:
                pass

result = Dict2Class(onecall_data)
'''
{'lat': 48.8833, 'lon': 2.5333, 'timezone': 'Europe/Paris', 'timezone_offset': 3600,
'current': {'dt': 1646742397, 'sunrise': 1646720300, 'sunset': 1646761399, 'temp': 10.42, 'feels_like': 8.69,
'pressure': 1016, 'humidity': 45, 'dew_point': -0.88, 'uvi': 2.56, 'clouds': 0, 'visibility': 10000, 'wind_speed': 5.14,
'wind_deg': 110, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}]},
'daily': [{'dt': 1646740800, 'sunrise': 1646720300, 'sunset': 1646761399, 'moonrise': 1646729040, 'moonset': 1646695320,
'moon_phase': 0.19, 'temp': {'day': 10.42, 'min': -0.1, 'max': 11.68, 'night': 6.35, 'eve': 9.04, 'morn': -0.1},
'feels_like': {'day': 8.69, 'night': 4.67, 'eve': 7.74, 'morn': -3.49}, 'pressure': 1016, 'humidity': 45, 'dew_point': -0.88,
'wind_speed': 4.4, 'wind_deg': 105, 'wind_gust': 11.61, 'weather': [{'id': 800, 'main': 'Clear',
'description': 'clear sky', 'icon': '01d'}], 'clouds': 0, 'pop': 0, 'uvi': 2.56},
{'dt': 1646827200, 'sunrise': 1646806576, 'sunset': 1646847892, 'moonrise': 1646816940, 'moonset': 1646785920, .....
'''
# printing the result
if debug: print("After Converting Dictionary to Class : ")
if debug: print(result.__dict__)  

# convert dict to class
current = Dict2Class(result.__dict__['current'])
if debug: print(current.weather)
if debug: print(current.temp, current.feels_like, current.feels_like,current.pressure,current.humidity,current.dew_point,current.uvi)


def show_attributes(name,class_):
    if debug: print(name+' :')
    for i in inspect.getmembers(class_):
        #if debug: print(i)
        # to remove private and protected
        # functions
        if not i[0].startswith('_'):
              
            # To remove other methods that
            # doesnot start with a underscore
            if not inspect.ismethod(i[1]): 
                if debug: print(i[0],':',i[1])

show_attributes('\nResult attribs',result)
show_attributes('\nCurrent attribs',current)

d = result.__dict__['daily']  # get a list of dictionaries
if debug: print('Dictionary day 0 (Keys)\n',d[0].keys())  # d[0} keys

if debug: print('\nAll 8-day dictionaries :\n')
for k in range(len(d)):
    if debug: print('Day',k,d[k])

# convert dictionary of day 0 to class
day0 = Dict2Class(d[0])   # d[0] is a dictionary, daily is a class
# get class attribute 'temp'
if debug: print('\nContents of day0.temp:',day0.temp)

show_attributes('\nDaily attribs', day0)

if debug: print('\nSome keys from dictionaries in d')
for k in range(len(d)):
    if debug: print(d[k]['moon_phase'], d[k]['temp'],d[k]['humidity'])
    

# pro.openweathermap.org/data/2.5/forecast/hourly? not OK not free
# base_url = 'https://pro.openweathermap.org/data/2.5/forecast/hourly?q=gagny&appid='+API_Key

# api.openweathermap.org/geo/1.0/direct? OK 
base_url = 'http://api.openweathermap.org/geo/1.0/direct?q=Paris&limit=5&appid='+API_Key

# api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt={cnt}&appid={API key} not OK not free
#base_url = 'https://api.openweathermap.org/data/2.5/forecast/daily?appid='+API_Key+'&lat='+str(lat)+'&lon='+str(lon)

request_data = requests.get(base_url).json()
if debug: pprint(request_data)

class onecall_class(object):
    '''convert all embedded dictionary to class attributes'''
    def __init__(self, my_dict):
        result =  Dict2Class(my_dict)
#         self.t_day = []
#         self.t_eve = []
#         self.t_morning = []
#         t_day = []
#         t_eve = []
#         t_morning = []
        for k in result.__dict__.keys():
            #print('Key :',k, result.__getattribute__(k))
            
            value = result.__getattribute__(k)
            if isinstance(value, dict):
                #if debug: print('--------------------------------------------------')
                #if debug: print('Instancing with', value)
                setattr(self, k, Dict2Class(value))
            elif isinstance(value, list):
                #print(value,'>>>>>',len(value))
                #if debug: print('++++++++++++++++++++++++++++++++++++++++++++++++++')
                #print('List of',len(value),'dictionaries computing', value)
                if len(value)==1:
                    #print('line138',value,'\n***',value[0])
                    #if isinstance(value[0], list):
                    setattr(self, k, value[0])
                    #elif isinstance(value[0], dict):
                    #    setattr(self, k, onecall_class(value[0]))
                else:
                    #t_day = []
                    for i,d in enumerate(value):
                        #if debug: print('***** day',i)
                        setattr(self, k+str(i), onecall_class(d))
                        #try:
                        c = self.__getattribute__(k+str(i))
                        #if debug: print('***************')
                        #if debug: print(d['dt'],dir(c),c.dt)
                        #if debug: print(c.temp.day)
#                         t_eve.append(c.temp.eve)
#                         t_morning.append(c.temp.morn)
#                         t_day.append(c.temp.day)
                        #t_day.append(c.temp.day)
                        #except:
                        #    pass
                    
                #if debug: print('++++++++++++++++++++++++++++++++++++++++++++++++++')
            else:
                setattr(self, k, value)
        
#         self.t_day = t_day
#         self.t_eve = t_eve
#         self.t_morning = t_morning
        
    def get_temperature(self):
        t_day = []
        t_min = []
        t_max =[]
        t_night = []
        t_eve = []
        t_morn = []
        for k in range(8):
            t_day.append(self.__dict__['daily'+str(k)].__dict__['temp'].__dict__['day'])
            t_min.append(self.__dict__['daily'+str(k)].__dict__['temp'].__dict__['min'])
            t_max.append(self.__dict__['daily'+str(k)].__dict__['temp'].__dict__['max'])
            t_night.append(self.__dict__['daily'+str(k)].__dict__['temp'].__dict__['night'])
            t_eve.append(self.__dict__['daily'+str(k)].__dict__['temp'].__dict__['eve'])
            t_morn.append(self.__dict__['daily'+str(k)].__dict__['temp'].__dict__['morn'])
        return t_day, t_min, t_max, t_night, t_eve, t_morn


# if debug: print('Keys :',onecall_data.keys())
# if debug: print('Current dictionary ;',onecall_data['current'])
# if debug: print('daily key contents :',onecall_data['daily'])

if debug: print('\n\nConverting to class ......')
cl = onecall_class(onecall_data)

if debug: print('--------------------------------------------------')
if debug: print(dir(cl))
if debug: print('Lat:',cl.lat)
if debug: print('Day 0:',dir(cl.daily0))
if debug: print('Day 0:',cl.daily0.weather.__dict__)
if debug: print('Day 0:',cl.daily0.temp.__dict__)
if debug: print('Day 0 temperature:',cl.daily0.weather.description)
if debug: print('Day 1 temperature:',cl.daily1.temp.day)

if debug: print(cl.__dict__['daily0'].__dict__)
if debug: print(cl.__dict__['daily0'].__dict__['temp'].__dict__)
if debug: print(cl.__dict__['daily0'].__dict__['weather'].__dict__)

for k in range(8):
    if debug: print(cl.__dict__['daily'+str(k)].__dict__['temp'].__dict__['day'])
    
t_day,t_min, t_max, t_night, t_eve, t_morn = cl.get_temperature()
if debug: print(t_day,t_min, t_max, t_night, t_eve, t_morn)

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

now = dt.datetime.now()
then = now + dt.timedelta(days=8)
days = mdates.drange(now,then,dt.timedelta(days=1))

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
plt.gcf().autofmt_xdate()

x = days
y = t_day
plt.plot(days,y,label='t_day')
y = t_max
plt.plot(x,y,label='t_max')
y = t_min
plt.plot(x,y,label='t_min')
y = t_night
plt.plot(x,y,label='t_night')
y = t_eve
plt.plot(x,y,label='t_eve')
y = t_morn
plt.plot(x,y,label='t_morn')
plt.plot(days[0],current.temp,'ro',label='current temp')
plt.grid()
plt.legend()
plt.title('Current temp : '+str(current.temp)+' °C')
plt.show()
