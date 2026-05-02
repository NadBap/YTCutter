import json
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import webbrowser
from BackEnd.file_utils import resource_path as rp

def main():
    master = Tk()

    YTlink = StringVar()
    FormatVar = StringVar()
    LoadingSpriteVar = StringVar()
    FOptions = {"Video": 1, "Audio": 2, "Video+Audio": 3}
    
    json_path = rp("Util/user-experience.json")
    with open(json_path, 'r') as file:
        jsoncontrol = json.load(file)
        
    result = {}
    listLoadingSprites = os.listdir(rp("Util/Sprite/LoadingSprite"))

    def settingClick():
        pass
    
    
    def ExitClick(name=None):
        if name == "clip":
            result["isClipping"] = True
        else:
            result["isClipping"] = False
        result["link"] = YTlink.get()
        result["filepath"] = filedialog.askdirectory()
        result["selection"] = FOptions[FormatVar.get()]
        result["x"] = master.winfo_x()
        result["y"] = master.winfo_y()
        result["LoadingSprite"] = LoadingSpriteVar.get()
        if result["link"] == '':
            link.pack(after=formatOption)
        else:
            master.destroy()

    # Window Config
    master.geometry("400x300")
    master.title("YTCutter")
    master.resizable(False, False)

    icon = PhotoImage(file=rp("Util/Sprite/Icon.png"))
    master.iconphoto(True, icon)

    # Basic UI creation
    Title = Label(master, text="YTCutter")
    Title.config(font= ("Impact", 25))

    TitleSubText = Button(master, text="GitHub Repo", borderwidth=0, command= lambda: webbrowser.open_new("github.com/nadbap/YTCutter")
                        , foreground="blue", underline=True, font=("Arial", 10))
    
    h2 = Label(master, text="Enter YT link and download it :)")
    h2.config(font= ('Impact', 15))

    Link = Entry(master, width=50, bg="light grey", textvariable=YTlink, font=("Times New Roman", 10, "normal")
                , bd=2)

    Download = Button(master, text="Download", width=20, activebackground="light gray",
                command=lambda: ExitClick("Download"))
    
    Clip = Button(master, text="Clip", width=20, activebackground="light gray",
            command=lambda: ExitClick("clip"))
    
    settingsImg = PhotoImage(file=rp("Util/Sprite/Gear.png"))
    settingsButton = Button(master, image=settingsImg, borderwidth=0, command=lambda: messagebox.showinfo("NAHH", message="Doesnt work rn ¯\_(ツ)_/¯"))
    
    MoreFromMe = Button(master, text="More From Me", borderwidth=0, command= lambda: webbrowser.open_new("https://sites.google.com/view/nadbap/home?authuser=0")
                        , foreground="blue", underline=True)
    
    link = Label(master, text="Please input a valid link")
    link.config(font= ('Arial', 9), fg="red")
    
    formatOption = ttk.Combobox(master, values=["Video+Audio", "Audio", "Video"], textvariable= FormatVar, state="readonly")
    formatOption.set("Video+Audio")
    
    listLoadingSpritesNew = [jsoncontrol["loading_bar"]["loaded_sprite"]]
    print(listLoadingSprites)
    for i in listLoadingSprites:
        if i != jsoncontrol["loading_bar"]["loaded_sprite"]:
            listLoadingSpritesNew.append(i)  
            
    spriteOption = ttk.Combobox(master, textvariable= LoadingSpriteVar, state="readonly")
    spriteOption['values'] = listLoadingSpritesNew
    # spriteOption.set(jsoncontrol["loading_bar"]["loaded_sprite"])
    
   
    
    spriteOption.set(listLoadingSpritesNew[0])

   
    Title.pack(fill="both", pady=[5,0])
    TitleSubText.pack(fill="both")
    h2.pack()
    formatOption.pack()
    Link.pack(pady=[10, 20])  
    Download.pack()
    Clip.pack()
    spriteOption.pack(pady=5)
    settingsButton.pack(side=["right"],  padx=[0, 5], pady=[0, 5])
    MoreFromMe.pack(side=["left"], padx=[5, 0], pady=[0, 5])
    '''
    master.columnconfigure(0, weight=1)
    master.columnconfigure(1, weight=1)
    master.columnconfigure(2, weight=1)

    settingsButton.grid( padx=[0, 5], pady=[5, 0], sticky="e")
    Title.grid(sticky="nesw", pady=[0, 5], row=1, column=1)
    h2.grid(row=2, column=1)
    formatOption.grid()
    Link.grid(pady=[10, 20])  
    Download.grid()
    Clip.grid()
    spriteOption.grid(pady=5)
    '''
    # Make screen appear
    master.mainloop()
    return result


if __name__ == "__main__":
    ello = main()
    print(ello) 