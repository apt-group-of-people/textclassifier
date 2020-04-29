from tkinter import *


LARGE_FONT = ("Verdana", 12, "bold")
BUTTON_FONT = ("Verdana", 10)

class ProjectApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        Tk.iconbitmap(self, default="icon.ico")
        Tk.wm_title(self, "Project Application")

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (Guide, GatherData, Toolbar):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nswe")
        
        self.show_frame(Guide)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



class Toolbar(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        Frame.bg="#4285f4"
        btn1 = Button(self, text="Guide", font=BUTTON_FONT, bd=1, bg="#4285f4", fg="white", command=lambda: controller.show_frame(Guide))
        btn2 = Button(self, text="Gather Data", font=BUTTON_FONT, bd=1, bg="#4285f4", fg="white", command=lambda: controller.show_frame(GatherData))
        btn3 = Button(self, text="Data Processing and Cleaning", font=BUTTON_FONT, bd=1, bg="#4285f4", fg="white", command=lambda: controller.show_frame(Guide))
        btn4 = Button(self, text="Data Training", font=BUTTON_FONT, bd=1, bg="#4285f4", fg="white", command=lambda: controller.show_frame(GatherData))
        btn5 = Button(self, text="Classification", font=BUTTON_FONT, bd=1, bg="#4285f4", fg="white", command=lambda: controller.show_frame(Guide))
        btn6 = Button(self, text="Visualization", font=BUTTON_FONT, bd=1, bg="#4285f4", fg="white", command=lambda: controller.show_frame(GatherData))
        btn1.pack(side=LEFT)
        btn2.pack(side=LEFT)
        btn3.pack(side=LEFT)
        btn4.pack(side=LEFT)
        btn5.pack(side=LEFT)
        btn6.pack(side=LEFT)
    

class Guide(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.app_toolbar = Toolbar(self, controller)
        titleFrame = Frame(self, bg="#4285f4")
        title = Label(titleFrame, text="Guide", fg="white", bg="#4285f4", font=LARGE_FONT)
        self.app_toolbar.pack(anchor="nw")
        title.pack()
        titleFrame.pack(fill=BOTH)
        
    
class GatherData(Frame):
    def __init__ (self, parent, controller):
        Frame.__init__(self, parent)
        titleFrame = Frame(self, bg="#4285f4")
        title = Label(titleFrame, text="Gather Data", fg="white", bg="#4285f4", font=LARGE_FONT)
        self.app_toolbar = Toolbar(self, controller)
        self.app_toolbar.pack(anchor="nw")
        title.pack()
        titleFrame.pack(fill=BOTH)

app = ProjectApp()
app.mainloop()