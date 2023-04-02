# Weather Interface

"""
This program is to take an input of a location name and output weather information for that area
This has the ability to show current weather information or daily weather information for a week
Hourly information has been implemented in the background but does not work as my API key does not have access to that function

This program was made as it allowed me to learn more about API's and how to interact with them
"""


from frameCurrent import *
from frameDaily import *
import tkinter as tk
from tkinter import ttk


class Window:
    def __init__(self, root, title, geometry):
        # This will set all of the base information to create the main window
        self.root = root
        self.root.title(title)
        self.root.geometry(geometry)
        # Universal variables
        pad_ext = 5

        # This will create the notebook for the entire program
        notebook_main = ttk.Notebook(master=root)
        notebook_main.pack(expand=1, fill='both', padx=pad_ext, pady=pad_ext)

        # To create the frames for each madin tab
        tab_current = tk.Frame(master=notebook_main)
        tab_daily = tk.Frame(master=notebook_main)
        # And to add these to the main notebook
        notebook_main.add(tab_current, text='Current Weather')
        notebook_main.add(tab_daily, text='7 Daily Weather')
        # Making configurations to the rows and columns
        tab_current.columnconfigure([0], weight=1)
        tab_daily.columnconfigure([0], weight=1)
        tab_current.rowconfigure([1], weight=1)
        tab_daily.rowconfigure([1], weight=1)


        # Putting all the frames into the main program now
        FrameCurrent(tab_current)
        FrameDaily(tab_daily)

        self.root.mainloop()  # To actually run the program loop


def main():
    window = Window(tk.Tk(), 'Weather Interface', '500x600')


main()


# Future Improvements
#   Current weather time is not displaying properly. It's showing the local data retrieval time, and not the actual time and date at that location.
