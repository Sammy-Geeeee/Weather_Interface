# This will define the FrameCurrent class, which will be used to display the current weather frame


from functions import *
import tkinter as tk
from tkinter import font
import os
from dotenv import load_dotenv
from datetime import datetime


class FrameCurrent(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Some base variables for the sizing of various things
        pad_ext = 5
        pad_int = 2

        # This will make the sub-frames within the current weather frame
        self.frame_input = tk.Frame(self.master)
        self.frame_output = tk.Frame(self.master)
        # To position these frames
        self.frame_input.grid(row=0, column=0, padx=pad_ext, pady=pad_ext, sticky='new')
        self.frame_output.grid(row=1, column=0, padx=pad_ext, pady=pad_ext, sticky='nsew')
        # Configurations for various parts 
        self.frame_input.columnconfigure([1], weight=1)
        self.frame_output.columnconfigure([0], weight=1)
        self.frame_output.rowconfigure([0], weight=1)

        # To make all the widgets within the current weather frame
        self.label_location = tk.Label(self.frame_input, text='Location')
        self.entry_location = tk.Entry(self.frame_input)
        self.scroll_info = tk.Scrollbar(self.frame_output)
        self.list_info = tk.Listbox(self.frame_output, yscrollcommand=self.scroll_info.set)
        self.button_clear = tk.Button(self.frame_input, text='Clear Output', command=lambda: self.list_info.delete(0, tk.END))
        # To position everything as it goes into the frame
        self.label_location.grid(row=0, column=0, padx=pad_ext, pady=pad_ext)
        self.entry_location.grid(row=0, column=1, padx=pad_ext, pady=pad_ext, sticky='ew')
        self.scroll_info.grid(row=0, column=1, padx=[0, pad_ext], pady=pad_ext, sticky='ns')
        self.list_info.grid(row=0, column=0, padx=[pad_ext, 0], pady=pad_ext, sticky='nsew')
        self.button_clear.grid(row=0, column=2, columnspan=2, padx=pad_ext, pady=pad_ext)
        # Configurations for various things
        self.scroll_info.config(command=self.list_info.yview)
        self.list_info.config(font=font.Font(size=11))

        # To bind pressing the enter key to performing a function
        self.entry_location.bind('<Return>', lambda event: self.postOutputs())



    def retrievelocation(self):
        # This is to retrieve all the data from the GUI inputs
        self.location = self.entry_location.get()

        return self.location
    

    def postOutputs(self):
        location = self.retrievelocation()
        load_dotenv()

        key = os.getenv('weatherbit_key')
        data = currentWeatherData(location, key)

        # This section will do some conversions so I don't put too much code in the display lines
        time = datetime.fromtimestamp(data['time_ob']).strftime('%A, %d %B - %H:%M')  # This will give the time in the specified format
        wind_spd = data['wind_spd'] * 3.6  # This will put the wind speed in km/hr

        
        # This section will now show all of the current weather data for the requested location
        self.list_info.insert(tk.END, f"Current Weather Data")
        self.list_info.insert(tk.END, f"{data['city_name']}, {data['country_code']} - {time}")  # TODO - This shows the time of data retrieval in the PC's timezone, and not the time of the actual place asked for
        self.list_info.insert(tk.END, data['time_local'])  # I have no idea what this is showing but I'm pretty sure it's not what I want it to
        self.list_info.insert(tk.END, data['weather'])
        self.list_info.insert(tk.END, f"Temp: {data['temp']} C    Feels Like: {data['feels_like']} C")
        self.list_info.insert(tk.END, f"Humidity: {data['humidity']} %")
        self.list_info.insert(tk.END, f"Cloud Cover: {data['cloud_cover']} %")
        self.list_info.insert(tk.END, f"Precipitation: {float(data['precip']):.1f} mm/hr")
        self.list_info.insert(tk.END, f"Wind Speed: {float(wind_spd):.1f} km/hr    Wind Direction: {data['wind_dir']}")
        self.list_info.insert(tk.END, f"UV Index: {float(data['uv_index']):.1f}")
        self.list_info.insert(tk.END, f"Snowfall: {data['snow']} mm/hr")

        self.list_info.insert(tk.END, '')  # To add a blank space before the next entry
        self.entry_location.delete(0, 'end')  # To clear the entry box
