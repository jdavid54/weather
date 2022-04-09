# https://www.youtube.com/watch?v=NCCYWIzN6hU
from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox

from timezonefinder import TimezoneFinder
import requests
import pytz
from datetime import datetime
from pprint import pprint
# to import phot from url
from urllib.request import urlopen
from PIL import Image, ImageTk

#API_Key = 'edffd1bf975a74d5d10e58c5ac8be2d3'
API_Key = 'c9d926a9549ae7933324ef26e13bb200'
#API_Key = '56040ff66d50184c81a4df3a770657e3'

root=Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False, False)


def get_image(icon):
    print(icon)
    try:
        #URL = "https://openweathermap.org/img/w/"+icon+".png"      # small icons
        URL = "https://openweathermap.org/img/wn/"+icon+"@2x.png"  # big icons
        print(URL)
        u = urlopen(URL)
        raw_data = u.read()
        u.close()

        # from github
        URL = "https://raw.githubusercontent.com/jdavid54/tkinter/main/Weather%20App/weather_icons/"+icon+"@2x.png" 
        print(URL)
        u = urlopen(URL)
        raw_data = u.read()
        u.close()
        
        # read from local file
#         file = 'weather_icons/'+icon+'@2x.png'
#         with open(file,'rb') as f:
#             raw_data = f.read()

        photo = ImageTk.PhotoImage(data=raw_data) # <-----

        label = tk.Label(image=photo)
        label.image = photo
        label.config(bg="lightgrey")
        label.place(x=700, y=150)
    except Exception as e:
        messagebox.showerror("Weather App","No weather icon found !!")

    
def getWeather():
    try:
        city=textfield.get()
        
        geolocator=Nominatim(user_agent="geoapiExercises")
        location=geolocator.geocode(city)
        obj= TimezoneFinder()
        result=obj.timezone_at(lng=location.longitude, lat=location.latitude)
        
        home=pytz.timezone(result)
        local_time=datetime.now(home)
        current_time=local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        name.config(text="CURRENT WEATHER")

        #weather
        api="https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+API_Key
        
        json_data=requests.get(api).json()
        pprint(json_data)
        condition = json_data['weather'][0]['main']
        description = json_data['weather'][0]['description']
        temp = round(json_data['main']['temp']-273.15,1)
        feel_like = round(json_data['main']['feels_like']-273.15,1)
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']
        icon = json_data['weather'][0]['icon']
        max_ = round(json_data['main']['temp_max']-273.15,1)
        min_ = round(json_data['main']['temp_min']-273.15,1)
        lat = round(json_data['coord']['lat'],2)
        dlat='N'
        if lat<0:
            lat=-lat
            dlat='S'
        lon = round(json_data['coord']['lon'],2)
        dlon='E'
        if lon<0:
            lon=-lon
            dlon='W'
        
        co.config(text=("Latitude:",lat,dlat,"-","Longitude:",lon,dlon))
        t.config(text=(temp,"°"))
        c.config(text=(condition,"|","FEELS","LIKE", feel_like,"°"))
        m.config(text=("MAX:",max_,"°","-","MIN:",min_,"°"))
        w.config(text=wind)
        h.config(text=humidity)
        d.config(text=description)
        p.config(text=pressure)
        get_image(icon)

    except Exception as e:
        messagebox.showerror("Weather App","Invalid Entry!!")
#icon
image_icon = PhotoImage(file="logo.png")
root.iconphoto(False, image_icon)

#search box
Search_image=PhotoImage(file="search.png")
myimage=Label(image=Search_image)
myimage.place(x=20,y=20)

city = 'gagny'
textfield=tk.Entry(root,justify="center",width=17,font=("poppins",25,"bold"),bg="#404040",border=0,fg="white")
textfield.place(x=50,y=40)
textfield.insert(0,city)
textfield.focus()


Search_icon=PhotoImage(file="search_icon.png")
myimage_icon=Button(image=Search_icon,borderwidth=0,cursor="hand2",bg="#404040",command=getWeather)
myimage_icon.place(x=400,y=34)

#logo
Logo_image = PhotoImage(file="logo.png")
logo=Label(image=Logo_image)
logo.place(x=150, y=100)

#Bottom box
Frame_image = PhotoImage(file="box.png")
frame_myimage=Label(image=Frame_image)
frame_myimage.pack(padx=5,pady=5,side=BOTTOM)

#time
name=Label(root,font=("arial",15,'bold'))
name.place(x=30,y=100)
clock=Label(root,font=("Helvetica",20))
clock.place(x=30,y=130)

#labels
label1=Label(root,text="WIND",font=("Helvetica",15,'bold'),fg="white",bg="#1ab5ef")
label1.place(x=120,y=400)

label2=Label(root,text="HUMIDITY",font=("Helvetica",15,'bold'),fg="white",bg="#1ab5ef")
label2.place(x=250,y=400)

label3=Label(root,text="DESCRIPTION",font=("Helvetica",15,'bold'),fg="white",bg="#1ab5ef")
label3.place(x=430,y=400)

label4=Label(root,text="PRESSURE",font=("Helvetica",15,'bold'),fg="white",bg="#1ab5ef")
label4.place(x=650,y=400)

# coords
co=Label(font=("arial",12,'bold'))
co.place(x=500,y=50)
#temperature
t=Label(font=("arial",70,'bold'),fg="#ee666d")
t.place(x=400,y=150)
#condition
c=Label(font=("arial",15,'bold'))
c.place(x=400,y=250)
#max min
m=Label(font=("arial",12,'bold'))
m.place(x=400,y=280)
#wind
w=Label(text="...",font=("arial",20,'bold'),bg="#1ab5ef")
w.place(x=120,y=430)
#humidity
h=Label(text="...",font=("arial",20,'bold'),bg="#1ab5ef")
h.place(x=280,y=430)
#description
d=Label(text="...",font=("arial",20,'bold'),bg="#1ab5ef")
d.place(x=400,y=430)
#pressure
p=Label(text="...",font=("arial",20,'bold'),bg="#1ab5ef")
p.place(x=670,y=430)

getWeather()
root.mainloop()