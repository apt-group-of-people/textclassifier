from tkinter import *
from tkcalendar import *
from tkinter import messagebox
import GetOldTweets3 as got

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
    keyword = ''
    tweetCount = 0
    startDate = ''
    endDate = ''

    def __init__ (self, parent, controller):
        Frame.__init__(self, parent)
        titleFrame = Frame(self, bg="#4285f4")
        title = Label(titleFrame, text="Gather Data", fg="white", bg="#4285f4", font=LARGE_FONT)
        app_toolbar = Toolbar(self, controller)
        app_toolbar.pack(anchor="nw")
        title.pack()
        titleFrame.pack(fill=BOTH)
        
        leftFrame = Frame(self)
        leftFrame.pack(side=LEFT, anchor="nw")
        keywordLabel = Label(leftFrame, text="Keywords(s) :")
        tweetCount = Label(leftFrame, text="No. of Tweets :")
        StartDate = Label(leftFrame, text="Start Date :")
        EndDate =  Label(leftFrame, text="End Data :")
        keywordLabel.grid(row=0, column=0)
        tweetCount.grid(row=1)
        StartDate.grid(row=2)
        EndDate.grid(row=3)

        keyword = StringVar()
        tweetCount = IntVar()

        keywordEntry = Entry(leftFrame, width=25, textvariable=keyword)
        tweetCount = Entry(leftFrame, width=25, textvariable=tweetCount)
        DateStart = DateEntry(leftFrame, width=22, background="white")
        DateEnd = DateEntry(leftFrame, width=22, background="white")
        DateStart.grid(row=2,column=1)
        DateEnd.grid(row=3, column=1)
        tweetCount.grid(row=1, column=1)
        keywordEntry.grid(row=0, column=1)

        def collect():
            self.keyword = str(keyword.get())
            self.tweetCount = int(tweetCount.get())
            self.startDate = str(DateStart.get_date())
            self.endDate = str(DateEnd.get_date())
            self.GetOldTweets(self.keyword, self.tweetCount, self.startDate, self.endDate)

        collectBtn = Button(leftFrame, text="Collect", bg="#4285f4", fg="white", width=21, command=collect)
        collectBtn.grid(row=4, column=1)
        clearBtn = Button(leftFrame, text="Clear", bg="#4285f4", fg="white", width=21)
        clearBtn.grid(row=5, column=1)

    def GetOldTweets(self,keyword, count, start, end):
        tweetCriteria = got.manager.TweetCriteria()\
                .setQuerySearch(keyword)\
                .setSince(start)\
                .setUntil(end)\
                .setMaxTweets(count)
        tweets = got.manager.TweetManager.getTweets(tweetCriteria)
        text_tweets = [[tweet.text] for tweet in tweets]
        dataFile = FileHandling('tweets.txt', text_tweets)

class FileHandling:
    def __init__(self, parent, tweets):
        self.File = open(parent, "w+", encoding='utf-8')
        self.handleFile(tweets)
        self.File.close()
        
    def handleFile(self, tweets):
        text = ""
        for i in range(0, len(tweets)):
            text = tweets[i][0] + '\n' + text
            self.File.write(text)

        


app = ProjectApp()
app.mainloop()