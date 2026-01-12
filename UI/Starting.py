from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
from UI.LoadingBar import resource_path as rp

def main():
    master = Tk()

    YTlink = StringVar()
    FormatVar = StringVar()
    LoadingSpriteVar = StringVar()
    FOptions = {"Video": 1, "Audio": 2, "Video+Audio": 3}
    
    result = {}
    listLoadingSprites = os.listdir(rp("Util/Sprite/LoadingSprite"))

    def ExitClick(name=None):
        result["link"] = YTlink.get()
        result["filepath"] = filedialog.askdirectory()
        result["selection"] = FOptions[FormatVar.get()]
        result["button"] = name
        result["x"] = master.winfo_x()
        result["y"] = master.winfo_y()
        result["LoadingSprite"] = LoadingSpriteVar.get()
        master.destroy()

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
                command=lambda: ExitClick("Download"))
    
    formatOption = ttk.Combobox(master, values=["Video+Audio", "Audio", "Video"], textvariable= FormatVar, state="readonly")
    formatOption.set("Video+Audio")
    
    spriteOption = ttk.Combobox(master, textvariable= LoadingSpriteVar, state="readonly")
    spriteOption['values'] = listLoadingSprites
    spriteOption.set(listLoadingSprites[0])

    Title.pack()
    h2.pack()
    formatOption.pack()
    Link.pack(pady=25)  
    Download.pack()
    spriteOption.pack(pady=5)
    # Make screen appear
    master.mainloop()
    return result


if __name__ == "__main__":
    ello = main()
    print(ello) 