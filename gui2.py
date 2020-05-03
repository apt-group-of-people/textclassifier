from tkinter import *

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame=None
        self.switch_frame(FirstPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destry()
        self._frame = new_frame
        self._frame.pack()
    
class Toolbar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        btn1 = Button(self, text="Guide", bg="#4285f4", fg="white", command=lambda: master.show_frame(Guide))
        btn2 = Button(self, text="Gather Data", bg="#4285f4", fg="white", command=lambda: master.show_frame(GatherData))
        btn3 = Button(self, text="Data Processing and Cleaning", bg="#4285f4", fg="white", command=lambda: master.show_frame(Guide))
        btn4 = Button(self, text="Data Training", bg="#4285f4", fg="white", command=lambda: master.show_frame(GatherData))
        btn5 = Button(self, text="Classification", bg="#4285f4", fg="white", command=lambda: master.show_frame(Guide))
        btn6 = Button(self, text="Visualization", bg="#4285f4", fg="white", command=lambda: master.show_frame(GatherData))
        btn1.pack(side=LEFT)
        btn2.pack(side=LEFT)
        btn3.pack(side=LEFT)
        btn4.pack(side=LEFT)
        btn5.pack(side=LEFT)
        btn6.pack(side=LEFT)

class FirstPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        toolbar = Toolbar(self)
        toolbar.pack()
        title = Label(self, text="Guide", fg="white", bg="#4285f4")
        title.pack()



if __name__ == "__main__":
    app = App()
    app.mainloop()