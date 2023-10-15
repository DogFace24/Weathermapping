import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from datetime import datetime
import os

win = tk.Tk()
win.geometry("300x300")
win.title("Weather app")

#setting the icon
ico = Image.open('sun.jpg')
photo = ImageTk.PhotoImage(ico)
win.wm_iconphoto(False, photo)

my_file = open("C:\\Code\\weatherapp\\countries.txt", "r")
country_list = my_file.read().split("\n")
my_file.close()

fr1 = tk.Frame(win)

city_label = tk.Label(fr1, text="Enter your city: ")
city_label.grid(row = 0, column=0)

city_entry = tk.Entry(fr1)
city_entry.grid(row=0, column=1)

fr1.pack()

fr2 = tk.Frame(win)

country_label = tk.Label(fr2, text = "Choose a country")
country_label.grid(row=0, column=0)

def show(): 
    tk.label.config(text = clicked.get()) 

clicked = tk.StringVar() 

clicked.set("India") 

drop = ttk.Combobox(master = fr2 ,textvariable=clicked)

def check_input(event):
    value = event.widget.get()

    if value == '':
        drop['values'] = country_list
    else:
        data = []
        for item in country_list:
            if value.lower() in item.lower():
                data.append(item)

        drop['values'] = data

drop["values"] = country_list
drop.bind('<KeyRelease>', check_input)

drop.grid(row=0, column=1)

fr2.pack(pady=10)

def open_past_searches():
    os.startfile("C:\\Code\\weatherapp\\past_searches")

menubar = tk.Menu(win)
options_menu = tk.Menu(menubar, tearoff=0)
options_menu.add_command(label = "Past Searches ->", command=open_past_searches)
options_menu.add_command(label = "Close Program :'(", command = win.quit)
menubar.add_cascade(label = 'Options', menu=options_menu)

win.config(menu=menubar)

def go():

    win.geometry("1300x700")

    try: 
        mapquest_key = "key"
        weather_key = "key"

        display_loc = city_entry.get()+", "+drop.get()
        loc = display_loc.replace(" ", "")


        url = f"https://www.mapquestapi.com/geocoding/v1/address?key={mapquest_key}&location={loc}"

        r = requests.get(url)
        data = r.json()['results'][0]['locations'][0]['displayLatLng']
        lat = data['lat']
        lng = data['lng']

        data_label = tk.Label(win, text =f"The coordinates of {display_loc} are latitude: {lat} and longitude: {lng}", font=("Helvetica 24"))
        data_label.pack(pady = 10)

        weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={weather_key}&units=metric'

        r2 = requests.get(weather_url)
        w_data = r2.json()

        data_weather = w_data['weather'][0]
        data_temp = w_data['main']

        temp_label = tk.Label(win, text = "Temperature Details", font=("Helvetica 20"))
        temp_label.pack()

        for e, val in data_temp.items():
            if e == 'pressure':
               cur_label = tk.Label(win, text = f"{e}: {val} hPa", font = "Helvatica 15")
            elif e == 'humidity':
                cur_label = tk.Label(win, text = f"{e}: {val}%", font = "Helvatica 15")
            elif e == 'temp' or e == 'temp_max' or e == 'temp_min' or e == 'feels_like':
                cur_label = tk.Label(win, text = f"{e}: {val} *C",font = "Helvatica 15")
            elif e == 'sea-level' or 'grnd-level':
                cur_label = tk.Label(win, text = f"{e}: {val} metres", font = "Helvatica 15")
            
            cur_label.pack()

        weather_label = tk.Label(win, text = "Other Details", font=("Helvetica 20"))
        weather_label.pack(pady = 30)

        for e, val in data_weather.items():
           if e == 'id' or e == 'icon':
               continue
           cur_label = tk.Label(win, text = f"{e}: {val}", font = "Helvatica 15")
           cur_label.pack()

        now = datetime.now()
        name = now.strftime("%b-%d-%Y %H_%M_%S")

        with open(f"past_searches\\{display_loc}_{name}.txt", 'w') as f:
            f.write(f"Location: {display_loc}\n")
            f.write(f"Co-ordinates- Latitude:{lat}, Longitude:{lng} \n\n")
            f.write("--TEMPERATURE DETAILS--\n")
            for e, val in data_temp.items():
                f.write(f"{e}: {val} \n")
            f.write("\n--OTHER DETAILS--\n")
            for e, val in data_weather.items():
                f.write(f"{e}: {val} \n")
        
        f.close()

    except Exception as e:
        messagebox.showerror('Error!', "City and country don't match! (or we can't find it.)")
        print(e)


go_button = tk.Button(win, text = "Go!", command = go)
go_button.pack(pady = 15)

win.mainloop()