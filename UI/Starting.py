from tkinter import *
from tkinter import ttk

from BackEnd import Downloader as ddd
# Initilize the Tkinter
master = Tk()

YTlink = StringVar()
num = 0

options = {"Video": 1, "Audio": 2, "Video+Audio": 3}

def on_select(option):
    num = num
    selected_text = option.get()  # Get selected text
    selected_value = options.get(selected_text, None)  # Get corresponding value
    if selected_value is not None:
        num = options.get(selected_text, None)
        
# Window Config
master.geometry("400x300")

# Basic UI creation
Title = Label(master, text="NadBap YTCutter")
Title.config(font= ("Impact", 25))

h2 = Label(master, text="Enter YT link and download it :)")
h2.config(font= ('Impact', 15))

Link = Entry(master, width=50, bg="light grey", textvariable=YTlink, font=("Times New Roman", 10, "normal")
             , bd=2)

Enter = Button(master, text="Enter", width=20, activebackground="light gray",
               command=ddd.main(YTlink, num))

Options = ttk.Combobox(master, values=["Video+Audio", "Audio", "Video"], textvariable= n)
Options.set("Video+Audio")
Options.bind("<<ComboboxSelected>>", on_select(Options))

Title.pack()
h2.pack()
Options.pack()
Link.pack(pady=25)  
Enter.pack()
# Make screen appear
master.mainloop()