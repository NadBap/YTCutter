from tkinter import *
from tkinter import ttk

def main():
    master = Tk()
    
    master.geometry("300x100")
    
    Title = Label(master, text="FINISHED DOWNLOAD")
    Title.config(font= ("Impact", 25))
    
    Download = Button(master, text="Download", width=20, activebackground="light gray",
                command=lambda: ExitClick("Download"))
    
    Title.pack()
    
    master.mainloop()
if __name__ == "__main__":
    ello = main()
    print(main)