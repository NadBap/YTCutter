from UI import Starting as Init
from UI import LoadingBar as lb
from BackEnd import Downloader as ddd
import threading

class MainApp:
    def __init__(self):
        '''
        data = Init()

        self.link = data["link"]
        self.filepath = data["filepath"]
        self.button = data["button"]
        self.selection = data["selection"]
        self.winx = data["x"]
        self.winy = data["y"]'''
        #or____________________
        self.data = Init.main()
    
    def LoadingBar(self):
        thread = threading.Thread(target=lb.main, args= (self.data["x"],self.data["y"],self.data["LoadingSprite"]))
        thread.start()
        return thread
        
    def Download(self, thread):
        Downloadcode = ddd.main(self.data["link"], self.data["selection"], self.data["filepath"], thread)
        if Downloadcode != 0:
            print("error code: " + str(Downloadcode))
            return Downloadcode
        else:
            return "Complete"

def main():
    #initializes the class and start the loading bar thread
    YTCutter = MainApp()
    thread = YTCutter.LoadingBar()
    
    if YTCutter.data["button"] == "Download":
        YTCutter.Download(thread)
    thread.join()
    
if __name__ == "__main__":
    main()
        