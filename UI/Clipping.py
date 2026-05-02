from tkinter import *
from tkinter import messagebox
from BackEnd.file_utils import resource_path as rp
def main(url=False):
        # Init
        master = Tk()  
        Start = StringVar()
        End = StringVar()
        Time = []
        value = None

        master.geometry("600x200")
        master.resizable(False, False)
        
        #Icon Creation
        icon = PhotoImage(file=rp("Util/Sprite/Icon.png"))
        master.iconphoto(True, icon)
        
        '''
        #Tried making options
        # x button = go back to clipping
        # Download = Download full video
        # Exit = Go back to starting
        
        def UserExit(userdecision, win):
            value = userdecision
            win.destroy()
            print(value)
            if value != None:
                master.destroy()
            else:
                master.grab_set()
                
        def messageWindow():
            master.attributes('-disabled', True)
            win = Toplevel()
            win.title('warning')
            message = "Do you want to download the full video or exit to main screen"
            Label(win, text=message).pack()
            
            Button(win, text='Download', command=lambda : UserExit(True, win)).pack()
            Button(win, text='Exit', command=lambda : UserExit(False, win)).pack()
            win.wait_window()
            print(master)
            master.attributes('-disabled', False)
            print(value)
            
            
        '''    
        
        def numberCallback(P):
            return str.isdigit(P) or P == "" 
        
        numbervcmd = (master.register(numberCallback))  
        # Gave up
        # Yes = Go back to starting
        # No = Go back to clipping
        def Exit():
            UserExit = messagebox.askyesno(message="Are you sure you want to exit?", title="No more Clipping?")
            if UserExit:
                master.destroy()
            
        master.protocol('WM_DELETE_WINDOW', Exit)
        
        # No longer needed but stretches text on resizing
        def update_label_width(event):
            h2.config(wraplength=event.width)
        
        # Splits the user answers and has differents answer based on it
        def ButtonPress():
            # Splits
            S = Start.get().split(":")
            E = End.get().split(":")
            
            # Checks if there its i n HH:MM:SS format
            if len(S) == 3 and len(E) == 3:
                S = int(S[2]) + (60 * int(S[1])) + (60 * 60 * int(S[0]))
                E = int(E[2]) + (60 * int(E[1])) + (60 * 60 * int(E[0]))
                
                # Checks if Starting time is less the Ending time
                if S >= E:
                    IncorrectEntry.config(text="The start time CANNOT be lower or equal to the end time")
                    IncorrectEntry.pack(after=h2)
                    return
                Time.append(S)
                Time.append(E)
                master.destroy()
                
            else:
                IncorrectEntry.config(text="Please enter both times in HH:MM:SS (Enter 00 if no time)")
                IncorrectEntry.pack(after=h2)

        # UI Creation
        Title = Label(master, text="Clip Time")
        Title.config(font=("Impact", 25))

        
        h2 = Label(master, text="Enter the time frame of when you want to clip the video 'use HH:MM:SS'")
        h2.config(font=('Impact', 15))

        idek = Label(master, text="Start")
        idek.config(font=('Impact', 10))

        idke = Label(master, text="End")
        idke.config(font=('Impact', 10))

        IncorrectEntry = Label(master)
        IncorrectEntry.config(font= ('Arial', 9), fg="red")
        
        StartTime = Entry(master, width=10, bg="light grey", textvariable=Start, validate="all", 
                          font=("Times New Roman", 10, "normal"), bd=2, validatecommand=(numbervcmd, '%P'))
        
        EndTime = Entry(master, width=10, bg="light grey", textvariable=End, validate="all",
                        font=("Times New Roman", 10, "normal"), bd=2, validatecommand=(numbervcmd, '%P'))

        Enter = Button(master, text="Clip", width=20, activebackground="light gray", command=ButtonPress)

        #Packing
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

        
        if Time != []:
            return Time[0], Time[1]
        else:
            # Just to tell main to restart the code
            return 1,2 

if __name__ == "__main__":
    ello = main()
    print(ello)
