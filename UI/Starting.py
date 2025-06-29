from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import  threading

from BackEnd import Downloader as ddd
from BackEnd import Clip as ccc
from UI import ClipTIme as ct
from UI import LoadingBar as lb

def main():
    master = Tk()

    YTlink = StringVar()
    num = 3
    n = StringVar()
    options = {"Video": 1, "Audio": 2, "Video+Audio": 3}

    def on_select(event):
        global num
        selected_text = n.get()  # Get selected text
        selected_value = options[selected_text]  # Get corresponding value
        num = selected_value
        
    def DownloadClick():
        ConvertLink = Link.get()
        filepath = filedialog.askdirectory()
        thread = threading.Thread(target=lb.main, args= (master.winfo_x(), master.winfo_y()))
        thread.start()
        master.destroy()
        ddd.main(ConvertLink, num, filepath, thread)
        thread.join()
        
    '''
    def ClipClick():
        ConvertLink = Link.get()
        filepath = filedialog.askdirectory()
        Time = ct.main()
        thread = threading.Thread(target=lb.main, args= (master.winfo_x(), master.winfo_y()))
        thread.start()
        master.destroy()
        ccc.main(ConvertLink, num, filepath, Time[0], Time[1], thread)
        thread.join()
    '''
    # Window Config
    master.geometry("400x300")

    # Basic UI creation
    Title = Label(master, text="NadBap YTCutter")
    Title.config(font= ("Impact", 25))

    h2 = Label(master, text="Enter YT link and download it :)")
    h2.config(font= ('Impact', 15))

    Link = Entry(master, width=50, bg="light grey", textvariable=YTlink, font=("Times New Roman", 10, "normal")
                , bd=2)

    Download = Button(master, text="Download", width=20, activebackground="light gray",
                command=DownloadClick)
    
    # Clip = Button(master, text="Clip", width=20, activebackground="light gray",
 #                command=ClipClick)

    Options = ttk.Combobox(master, values=["Video+Audio", "Audio", "Video"], textvariable= n)
    Options.set("Video+Audio")
    Options.bind("<<ComboboxSelected>>", on_select)

    Title.pack()
    h2.pack()
    Options.pack()
    Link.pack(pady=25)  
    Download.pack()
    # Clip.pack()
    # Make screen appear
    master.mainloop()
if __name__ == "__main__":
    main()