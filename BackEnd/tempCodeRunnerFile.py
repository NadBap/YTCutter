# Source - https://stackoverflow.com/a
# Posted by OysterShucker, modified by community. See post 'Timeline' for change history
# Retrieved 2026-01-24, License - CC BY-SA 4.0

import tkinter as tk, re

class TimeEntry(tk.Entry):
    def __init__(self, master, **kwargs):
        tk.Entry.__init__(self, master, **kwargs)
        vcmd = self.register(self.validate)
        
        self.bind('<Key>', self.format)
        self.configure(validate="all", validatecommand=(vcmd, '%P'))

        self.valid = re.compile('^\d{0,2}(:\d{0,2}(:\d{0,2})?)?$', re.I)

    def validate(self, text):
        if ''.join(text.split(':')).isnumeric():
            return not self.valid.match(text) is None
        return False

    def format(self, event):
        if event.keysym != 'BackSpace':
            i = self.index('insert')
            if i in [2, 5]:
                if self.get()[i:i+1] != ':':
                    self.insert(i, ':')


class Main(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        TimeEntry(self, width=8).grid(row=0, column=0)


if __name__ == "__main__":
    root = Main()
    root.geometry('800x600')
    root.title("Time Entry Example")
    root.mainloop()
