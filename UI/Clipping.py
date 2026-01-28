from tkinter import *
import os
import subprocess
def main(url):
  # 
        master = Toplevel()  # <-- change Tk() to Toplevel()
        Start = StringVar()
        End = StringVar()
        Time = []

        ytdlp_path = os.path.join(os.path.dirname(__file__), "..", "Util", "yt-dlp.exe")

        command = [ytdlp_path, f"{url}", "--get-duration"]
        '''
        maxTime = subprocess.check_output(command)
        Length = maxTime.decode('utf-8')
        master.geometry("600x200")
        '''

    


        
        def update_label_width(event):
            h2.config(wraplength=event.width)
            
        def ButtonPress():
            Time.append(Start.get())
            Time.append(End.get())
            master.destroy()

        Title = Label(master, text="Clip Time")
        Title.config(font=("Impact", 25))

        h2 = Label(master, text="Enter the time frame of when you want to clip the video 'use HH:MM:SS'")
        h2.config(font=('Impact', 15))

        idek = Label(master, text="Start")
        idek.config(font=('Impact', 10))

        idke = Label(master, text="End")
        idke.config(font=('Impact', 10))

        StartTime = Entry(master, width=10, bg="light grey", textvariable=Start, font=("Times New Roman", 10, "normal"), bd=2, )
        EndTime = Entry(master, width=10, bg="light grey", textvariable=End, font=("Times New Roman", 10, "normal"), bd=2)

        Enter = Button(master, text="Clip", width=20, activebackground="light gray", command=ButtonPress)

        Title.pack()
        h2.pack(fill="both", expand=True)
        h2.bind("<Configure>", update_label_width)
        idek.pack(side="left")
        StartTime.pack(side="left", expand=True, fill=BOTH)
        idke.pack(side="left")
        EndTime.pack(side="left", expand=True, fill=BOTH)
        Enter.pack(side="bottom")

        master.grab_set()   # Make this window modal (forces user to interact with it)
        master.wait_window()  # Wait until this window closes before continuing
        ''' 
       if Time[0] > Time[1] or Time[0] < 0 or Time[1] >str(Length):
            print("Invalid")
        else:
        '''
        
        return Time[0], Time[1]

if __name__ == "__main__":
    main()
