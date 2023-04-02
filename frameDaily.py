# This will define the FrameDaily class, which will be used to display the daily weather frame


from functions import *
import tkinter as tk
from tkinter import font
import os
from dotenv import load_dotenv
from datetime import datetime



class FrameDaily(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Some base variables for the sizing of various things
        pad_ext = 5
        pad_int = 2

        # This will make the sub-frames within the daily weather frame
        self.frame_input = tk.Frame(self.master)
        self.frame_output = tk.Frame(self.master)
        # To position these frames
        self.frame_input.grid(row=0, column=0, padx=pad_ext, pady=pad_ext, sticky='new')
        self.frame_output.grid(row=1, column=0, padx=pad_ext, pady=pad_ext, sticky='nsew')
        # Configurations for various parts 
        self.frame_input.columnconfigure([1], weight=1)
        self.frame_output.columnconfigure([0], weight=1)
        self.frame_output.rowconfigure([0], weight=1)

        # To make all the widgets within the daily weather frame
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
        data = dailyWeatherData(location, key)

        self.list_info.insert(tk.END, f"7 Days Weather Data")
        self.list_info.insert(tk.END, f"{data[0]['city_name']}, {data[0]['country_code']}")
        self.list_info.insert(tk.END, '')  # To add a blank space
        
        for day in data:
            # This will do some conversions and data shortening for me so I don't have to do it so many times
            time = datetime.fromtimestamp(day['time']).strftime('%A, %d %B')  # This will give the time in the specified format
            sunrise = datetime.fromtimestamp(day['sunrise']).strftime('%H:%M')  # This will give the time in the specified format
            sunset = datetime.fromtimestamp(day['sunset']).strftime('%H:%M')  # This will give the time in the specified format
            wind_spd = day['wind_spd'] * 3.6
            

            # This will be the daily information that will be displayed
            self.list_info.insert(tk.END, f"{time}")
            self.list_info.insert(tk.END, f"Sunrise: {sunrise}    Sunset: {sunset}")
            self.list_info.insert(tk.END, day['weather'])
           
           
            self.list_info.insert(tk.END, f"Avg. Temp: {day['avg_temp']} C    Low: {day['min_temp']} C    High: {day['max_temp']} C")
            self.list_info.insert(tk.END, f"Humidity: {day['humidity']} %")
            self.list_info.insert(tk.END, f"Cloud Cover: {day['cloud_cover']} %")
            self.list_info.insert(tk.END, f"Precipitation: {float(day['precip']):.1f} mm/hr")
            self.list_info.insert(tk.END, f"Wind Speed: {float(wind_spd):.1f} km/hr    Wind Direction: {day['wind_dir']}")
            self.list_info.insert(tk.END, f"UV Index: {float(day['uv_index']):.1f}")
            self.list_info.insert(tk.END, f"Snowfall: {day['snow']} mm/hr")

            self.list_info.insert(tk.END, '')  # To add a blank space before the next entry
            self.entry_location.delete(0, 'end')  # To clear the entry box
