from tkinter import *
from tkinter import filedialog
from tkcalendar import *
from tkinter import messagebox
import GetOldTweets3 as got
from tkinter import ttk
import os 

from tweetcleaner import preprocess_tweet
from datapreprocess import *


LARGE_FONT = ("Verdana", 12, "bold")
BUTTON_FONT = ("Verdana", 10)
SIZE = '500x270'


class ProjectApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        Tk.iconbitmap(self, default="icon.ico")
        Tk.wm_title(self, "Text Classifier")
        self.geometry(SIZE)
        #self.resizable(0, 0)
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (Guide, GatherData, DataPC, Toolbar, Trainer, Classify):
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
        btn3 = Button(self, text="Cleaner", font=BUTTON_FONT, bd=1, bg="#4285f4", fg="white", command=lambda: controller.show_frame(DataPC))
        btn4 = Button(self, text="Trainer", font=BUTTON_FONT, bd=1, bg="#4285f4", fg="white", command=lambda: controller.show_frame(Trainer))
        btn5 = Button(self, text="Classifier", font=BUTTON_FONT, bd=1, bg="#4285f4", fg="white", command=lambda: controller.show_frame(Classify))
        btn6 = Button(self, text="Visualization", font=BUTTON_FONT, bd=1, bg="#4285f4", fg="white", command=lambda: controller.show_frame(Guide))
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
    filename = 'Choose a file'
    def __init__ (self, parent, controller):
        Frame.__init__(self, parent)
        titleFrame = Frame(self, bg="#4285f4")
        title = Label(titleFrame, text="Gather Data", fg="white", bg="#4285f4", font=LARGE_FONT)
        app_toolbar = Toolbar(self, controller)
        app_toolbar.pack(anchor="nw")
        title.pack()
        titleFrame.pack(fill=BOTH)

        btnName = 'Collect'
        leftFrame = Frame(self)
        leftFrame.pack(side=LEFT, anchor="nw")
        
        keywordLabel = Label(leftFrame, text="Keywords(s) :")
        tweetCount = Label(leftFrame, text="No. of Tweets :")
        StartDate = Label(leftFrame, text="Start Date :")
        EndDate =  Label(leftFrame, text="End Data :")
        #NameFile =  Label(leftFrame, text="File Name :")
        
        keywordLabel.grid(row=0, column=0)
        tweetCount.grid(row=1)
        StartDate.grid(row=2)
        EndDate.grid(row=3)
        #NameFile.grid(row=4)

        #namefile = StringVar()
        keyword = StringVar()
        tweetCount = IntVar()

        #filenameEntry = Entry(leftFrame, width=25, textvariable=namefile)
        keywordEntry = Entry(leftFrame, width=25, textvariable=keyword)
        tweetCount = Entry(leftFrame, width=25, textvariable=tweetCount)
        DateStart = DateEntry(leftFrame, width=22, background="white")
        DateEnd = DateEntry(leftFrame, width=22, background="white")
        
        # Initialize Value to none
        tweetCount.delete(0, "end")
        DateStart.delete(0, "end")
        DateEnd.delete(0, "end")

        #filenameEntry.grid(row=4,column=1, pady=(3, 3), sticky = W)
        DateStart.grid(row=2,column=1, pady=(3, 3), sticky = W)
        DateEnd.grid(row=3, column=1, pady=(3, 3), sticky = W)
        tweetCount.grid(row=1, column=1, pady=(3, 3), sticky = W)
        keywordEntry.grid(row=0, column=1, pady=(3, 3), sticky = W)

        def collect():
            #self.namefile = str(namefile.get())
            self.keyword = str(keyword.get())
            self.tweetCount = int(tweetCount.get())
            self.startDate = str(DateStart.get_date())
            self.endDate = str(DateEnd.get_date())
            self.GetOldTweets(self.keyword, self.tweetCount, self.startDate, self.endDate)
            

        def clearFieldsFn():
            keywordEntry.delete(0, END)
            tweetCount.delete(0, END)
        
        def handlefile():
            self.filename = FileHandling.filedialog(self)
            fileNameDisp = self.filename.split('/')
            fileNameDisp = fileNameDisp[-1]
            fileNameLabel.configure(text=fileNameDisp)

        collectBtn = Button(leftFrame, text=btnName, bg="#4285f4", fg="white", width=21, command=collect)
        collectBtn.grid(row=5, column=1, pady=(3, 3))
        clearBtn = Button(leftFrame, text="Clear", bg="#4285f4", fg="white", width=21, command=clearFieldsFn)
        clearBtn.grid(row=6, column=1, pady=(3, 3))

        rightFrame = Frame(self, background='black')
        rightFrame.pack(side=RIGHT, anchor="ne")
        
    def GetOldTweets(self,keyword, count, start, end):
        print('Collecting Tweets...')
        
        tweetCriteria = got.manager.TweetCriteria()\
                .setQuerySearch(keyword)\
                .setSince(start)\
                .setUntil(end)\
                .setMaxTweets(count)
        tweets = got.manager.TweetManager.getTweets(tweetCriteria)
        
        with open(FileHandling.file_save(self, '.txt'), 'w', encoding='utf-8') as new_collection:
            for tweet in tweets:
                new_collection.write(f'{tweet.text}\n')
        print(f'{len(tweets)} tweets successfuly collected!')


class DataPC(Frame):
    filename = 'Empty'
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.app_toolbar = Toolbar(self, controller)
        titleFrame = Frame(self, bg="#4285f4")
        title = Label(titleFrame, text="Cleaner", fg="white", bg="#4285f4", font=LARGE_FONT)
        self.app_toolbar.pack(anchor="nw")
        title.pack()
        titleFrame.pack(fill=BOTH)
        
        self.leftFrame = Frame(self)
        self.leftFrame.pack(side=LEFT, anchor="nw", padx=(15,0), pady=(15,0))
        
        self.newfile = StringVar()
        
        self.file = Label(self.leftFrame, text="File:")
        #self.newfilename = Label(self.leftFrame, text="New name:")

        #self.newfilename.grid(row=1, pady=(3, 3))

        #cleanedFile = Entry(self.leftFrame, width=35, textvariable=self.newfile)
        #cleanedFile.grid(row=1,column=1, pady=(3, 3), sticky = W)
        
        self.filenameLabel = Label(self.leftFrame, text=self.filename)
        self.filenameLabel.grid(row=0, column=1, pady=(3, 5), sticky = W)
        self.Buttons()

    def Buttons(self):
        def chooseFile():
            self.filename = FileHandling.filedialog(self, 'txt')
            if self.filename == '':
                fileNameDisp = self.filename
                self.filenameLabel.configure(text="Empty")
            else:
                fileNameDisp = self.filename
                self.filenameLabel.configure(text=fileNameDisp)

        def cleanfile():
            print('Cleaning...')
            temp = ''
            with open(str(self.filename), 'r', encoding="utf-8") as tweets:
                data = tweets.readlines()
                with open(FileHandling.file_save(self, '.txt'), 'w', encoding="utf-8") as newfile:
                  for x in data:
                    temp = preprocess_tweet(x)
                    newfile.write(f'{temp}\n')
            print('Cleaning Finished!')

        self.openFileBtn = Button(self.leftFrame, width=10, text = 'Select a file', command=chooseFile)
        self.cleanFile = Button(self.leftFrame, bg="#4285f4", fg="white", width=21, text = 'Clean the file', command=cleanfile)
        self.openFileBtn.grid(row=0, column=0, pady=(3, 5), sticky = W)
        self.cleanFile.grid(row=4, column=1, pady=(3, 3), sticky = W)


class Trainer(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.app_toolbar = Toolbar(self, controller)
        titleFrame = Frame(self, bg="#4285f4")
        title = Label(titleFrame, text="Trainer", fg="white", bg="#4285f4", font=LARGE_FONT)
        self.app_toolbar.pack(anchor="nw")
        title.pack()
        titleFrame.pack(fill=BOTH)
        
        self.leftFrame = Frame(self)
        self.leftFrame.pack(side=LEFT, anchor="nw", padx=(15, 0), pady=(10, 0))
        
        self.newfile = StringVar()
        self.wordcount = IntVar()
        
        self.words = Label(self.leftFrame, text="Num of words:")
        self.algo = Label(self.leftFrame, text="Algorithm:")

        self.words.grid(row=1, pady=(3, 3))
        self.algo.grid(row=2, pady=(3, 3))

        wordCount = Entry(self.leftFrame, width=25, textvariable=self.wordcount)
        wordCount.grid(row=1,column=1, pady=(3, 3), sticky = W)
        
        self.filenameLabel = Label(self.leftFrame, text='Empty...')
        self.filenameLabel.grid(row=0, column=1, pady=(3, 5), sticky = W)

        self.algoBox = ttk.Combobox(self.leftFrame, 
                            values=[
                                    "Naive Bayes", 
                                    "Support Vector Machine",
                                    "Decision Tree"],
                                    state="readonly", width=23)
        self.algoBox.grid(column=1, row=2, sticky = W)
        self.algoBox.current(0)
        self.Buttons()

    def Buttons(self):
        self.filepath = ''
        def chooseFile():
            self.filepath = FileHandling.filedialog(self, 'txt')
            if self.filepath == '':
                self.filepath = 'Empty'
            else:
                fileNameDisp = self.filepath 
                self.filenameLabel.configure(text=fileNameDisp)

        def trainData():
            print('Training...')
            algo = ''
            if str(self.algoBox.get()) == 'Naive Bayes':
                algo = 'naive'
            if str(self.algoBox.get()) == 'Support Vector Machine':
                algo = 'decision'
            if str(self.algoBox.get()) == 'Decision Tree':
                algo = 'svm'
                
            #print('test',algo)
            classifier_data, accuracy, update = classify_train(self.filepath, int(self.wordcount.get()), str(algo))

            f = FileHandling.file_save(self, '.pkl')
            pickle_out = open(f,"wb")
            pickle.dump(classifier_data, pickle_out)
            pickle_out.close()
            update.append('-----------Classifier Saved-------------\n\n')
            report = Tk()
            report.configure(bg='black')
            report.title("Training Result")
            
            mainTitle = Frame(report, bg="#4285f4")
            name = Label(mainTitle, text="Training Result", font=LARGE_FONT,fg="white", bg="#4285f4")
            name.pack()
            mainTitle.pack(fill=BOTH)

            mainBody = Frame(report)
            mainBody.pack(fill=BOTH)

            canvas = Canvas(mainBody)
            
            scrollbar = Scrollbar(mainBody, orient="vertical", command=canvas.yview)
            scrollable_frame = Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            i = 0
            for x in update:
                ttk.Label(scrollable_frame, text=x, justify=LEFT, anchor="w").grid(row=i, sticky = W)
                i = i+1
            mainBody.pack()
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
    

        self.openFileBtn = Button(self.leftFrame, width=10, text = 'Select the file', command=chooseFile)
        self.trainBtn = Button(self.leftFrame, bg="#4285f4", fg="white", width=22, text = 'Train', command=trainData)
        self.openFileBtn.grid(row=0, column=0, pady=(3, 3))
        self.trainBtn.grid(row=3, column=1, pady=(3, 5), sticky = W)


class Classify(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.app_toolbar = Toolbar(self, controller)
        titleFrame = Frame(self, bg="#4285f4")
        title = Label(titleFrame, text="Classify", fg="white", bg="#4285f4", font=LARGE_FONT)
        self.app_toolbar.pack(anchor="nw")
        title.pack()
        titleFrame.pack(fill=BOTH)
        
        self.leftFrame = Frame(self)
        self.leftFrame.pack(side=LEFT, anchor="nw", padx=(15, 0), pady=(10, 0))

        self.words = Label(self.leftFrame, text="New file:")


        self.filenameLabel = Label(self.leftFrame, text='Empty...')
        self.filenameLabel.grid(row=0, column=1, pady=(3, 5), sticky = W)

        self.classifierLabel = Label(self.leftFrame, text='Empty...')
        self.classifierLabel.grid(row=1, column=1, pady=(3, 5), sticky = W)

        self.Buttons()

    def Buttons(self):
        self.filename = ''
        self.classifier = ''
        def chooseFile():
            self.filename = FileHandling.filedialog(self, 'txt')
            if self.filename == '':
                fileNameDisp = 'Empty'
            else:
                self.filenameLabel.configure(text=self.filename)

        def chooseClassifier():
            self.classifier = FileHandling.filedialog(self, 'pickle')
            if self.classifier == '':
                fileNameDisp = 'Empty'
            else:
                self.classifierLabel.configure(text=self.classifier)

        def classifyTweets():
            print("Classifying data...")
            pickle_in = open(self.classifierLabel['text'],"rb")
            pickled_class = pickle.load(pickle_in)
            with open(self.filenameLabel['text'], 'r', encoding='ISO-8859-1') as tweetfile:
                with open(FileHandling.file_save(self, '.txt'), 'w+', encoding="utf-8") as saving:
                    for tweet in tweetfile:
                        #print(tweet)
                        saving.write(f"{tweet.strip()}\t{classify_data(pickled_class, tweet)}\n")
            pickle_in.close()

        self.selectFile = Button(self.leftFrame, width=15, text = 'Select the file', command=chooseFile)
        self.selectClassifier = Button(self.leftFrame, width=15, text = 'Select Classifier', command=chooseClassifier)
        self.classifyNow = Button(self.leftFrame, width=25, fg="white", bg="#4285f4", text = 'Classify Tweets', command=classifyTweets)
        self.selectFile.grid(row=0, column=0, pady=(3, 5), sticky = W)
        self.selectClassifier.grid(row=1, column=0, pady=(3, 3), sticky = W)
        self.classifyNow.grid(row=2, column=1, pady=(3, 3), sticky = W)
        
  
class FileHandling:
    def __init__(self, parent, tweets):
        self.File = open(parent, "w+", encoding='utf-8')
        self.handleFile(tweets)
        self.File.close()

    def filedialog(self, typ):
        file = set()
        if typ == 'txt':
            file = ("text", ".txt .text")
        elif typ == 'pickle':
            file = ("pickle", ".pickle .pkl")
            
        self.filename = filedialog.askopenfilename(initialdir = os.getcwd(), title = "Select A File", filetype = (file, ("All Files", "*.*")))   
        return self.filename

    def file_save(self, typ):
        file = set()
        if typ == '.txt':
            file = ("text", ".txt")
        elif typ == '.pkl':
            file = ("pickle", ".pkl")
        f = filedialog.asksaveasfile(initialdir = os.getcwd(), title = "Select A File", filetypes = [file], defaultextension=typ)
        if f is None:
            return
        return f.name

    def handleFile(self, tweets):
        text = ""
        for i in range(0, len(tweets)):
            text = tweets[i][0] + '\n' + text
            self.File.write(text)
        
app = ProjectApp()
app.mainloop()
