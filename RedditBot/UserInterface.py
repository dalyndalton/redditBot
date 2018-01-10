from tkinter import *

from bot import *

STICKY = N + E + S + W


class GUI(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("Reddit Analyzer by /u/itsthenewdx2")
        self.master.iconbitmap("Images/reddit_icon.ico")
        self.grid()

        # Variables
        self._upvoteCount = IntVar()
        self._downvoteCount = IntVar()
        self._numOfComments = IntVar()
        self._subredditName = StringVar()
        self._gildCount = IntVar()

        self._subSubDirectory = StringVar()
        self._listContents = StringVar()
        self._statusVar = StringVar()
        self._postTitle = StringVar()
        # The Reddit Bot
        try:
            self._bot = Redditbot()
            self._submissionlist = []
            self._subSubDirectory.set(self._bot._subreddit.display_name)
            self._statusVar.set("Connection successful! :D")
        except:
            self._statusVar.set("Connection unsuccessful.. :(")

        # Subreddit Label
        self._subredditLabel = Label(self, textvariable=self._subSubDirectory, relief='raised')
        self._subredditLabel.grid(row=0, column=0, sticky=STICKY)

        # Post Title Label
        self._postTitleLabel = Label(self, textvariable=self._postTitle, relief='raised', wrap=400)
        self._postTitleLabel.grid(row=0, column=1, sticky=STICKY)

        # Stats Label
        self._statLabel = Label(self, text="Misc Stats & info:", relief='raised')
        self._statLabel.grid(row=0, column=3, sticky=STICKY)

        # Listbox
        self._listBoxFrame = Frame(self)
        self._listBoxFrame.grid(row=1, column=0, sticky=STICKY)
        self._listYScroll = Scrollbar(self._listBoxFrame, orient=VERTICAL)
        self._listYScroll.grid(row=0, column=1, sticky=STICKY)
        self._ListBox = Listbox(self._listBoxFrame, listvariable=self._listContents,
                                yscrollcommand=self._listYScroll.set, width=28, height=15)
        self._ListBox.grid(row=0, column=0, sticky=STICKY)
        self._listYScroll['command'] = self._ListBox.yview
        self.populateListbox()

        self._selectButton = Button(self._listBoxFrame, text='SELECT', command=self.selectSubmission)
        self._selectButton.grid(row=1, column=0, columnspan=2, sticky=STICKY)

        # Post/Comment Contents & Stats
        ## Frame for it all
        self._postContentFrameName = StringVar()
        self._postContentFrameLabel = Label(textvariable=self._postContentFrameName)
        self._postContentFrame = Frame(self)
        self._postContentFrame.grid(row=1, column=1, sticky=STICKY)

        ## Entry Field
        self._contentFrameYScroll = Scrollbar(self._postContentFrame, orient=VERTICAL)
        self._contentFrameYScroll.grid(row=0, column=1, sticky=STICKY)
        self._contentBox = Text(self._postContentFrame, yscrollcommand=self._contentFrameYScroll, height=15, width=40,
                                wrap=WORD)
        self._contentBox.grid(row=0, column=0, sticky=STICKY)
        self._contentFrameYScroll['command'] = self._contentBox.yview

        ## SOMEHOW I FIGURED OUT HOW TO DISPLAY IMAGES FROM THE WEB SO IMA TRY THAT nvm
        self._image = PhotoImage()  # Placeholder
        self._imageDisplay = Label(self, relief='groove')
        self._imageDisplay.grid(row=1, column=2, sticky=STICKY)

        # Stat Frame
        self._statFrame = Frame(self)
        self._statFrame.grid(row=1, column=3, rowspan=2, sticky=STICKY)

        self._upvoteLabel = Label(self._statFrame, text="Upvotes:")
        self._upvoteLabel.grid(row=0, column=0)
        self._upvoteLabelCount = Label(self._statFrame, textvariable=self._upvoteCount)
        self._upvoteLabelCount.grid(row=0, column=1)

        self._downvoteLabel = Label(self._statFrame, text="Downvotes:")
        self._downvoteLabel.grid(row=1, column=0)
        self._downvoteLabelCount = Label(self._statFrame, textvariable=self._downvoteCount)
        self._downvoteLabelCount.grid(row=1, column=1)

        self._numCommentLabel = Label(self._statFrame, text="Comment Count:")
        self._numCommentLabel.grid(row=2, column=0)
        self._numCommentLabelCount = Label(self._statFrame, textvariable=self._numOfComments)
        self._numCommentLabelCount.grid(row=2, column=1)

        self._subredditNameLabel = Label(self._statFrame, text="Subreddit:")
        self._subredditNameLabel.grid(row=3, column=0)
        self._subredditNameLabelName = Label(self._statFrame, textvariable=self._subredditName)  # Great naming
        self._subredditNameLabelName.grid(row=3, column=1)

        self._gildLabel = Label(self._statFrame, text="Gilds:")
        self._gildLabel.grid(row=4, column=0)
        self._gildLabelCount = Label(self._statFrame, textvariable=self._gildCount)
        self._gildLabelCount.grid(row=4, column=1)

        # Sub Changer

        self._newSub = StringVar()
        self._subChangeFrame = Frame(self)
        self._subChangeFrame.grid(row=2, column=0, sticky=STICKY)
        self._newSubEntry = Entry(self._subChangeFrame, textvariable=self._newSub)
        self._newSubEntry.grid(row=0, column=0, sticky=STICKY)
        self._subChangeButton = Button(self._subChangeFrame, command=self.changeSubreddit, text="GO")
        self._subChangeButton.grid(row=0, column=1, sticky=STICKY)

        # Status Bar
        self._statusBar = Entry(self, state='disabled', textvariable=self._statusVar)
        self._statusBar.grid(row=3, column=0, columnspan=4, sticky=N + E + S + W)

    def updateStatus(self, status):
        self._statusVar.set(status)

    def populateListbox(self):
        self._submissionlist = self._bot.getSubmissionList()
        listoftitles = []
        listStr = ""
        for submission in self._submissionlist:
            if len(submission.title) > TITLE_LIMIT:
                listoftitles.append(submission.title[:TITLE_LIMIT] + "...")
            else:
                listoftitles.append(submission.title)
        self._listContents.set(listoftitles)

    def setStats(self, submission):
        self._upvoteCount.set(submission.ups)
        self._downvoteCount.set(submission.downs)
        self._numOfComments.set(submission.num_comments)
        self._gildCount.set(submission.gilded)
        self._subredditName.set(submission.subreddit_name_prefixed)

    def getImage(self, submission):
        image = self._bot.getPostImage(submission)
        if image is None:
            self._image = PhotoImage()
        else:
            self._image = image
            self._imageDisplay['image'] = self._image

    def selectSubmission(self):
        try:
            index, = self._ListBox.curselection()
        except ValueError:
            return
        self._contentBox.delete("1.0", END)
        submission = self._submissionlist[index]
        if len(submission.title) > float('inf'):
            self._postTitle.set(submission.title[:25] + "...")
        else:
            self._postTitle.set(submission.title)
        if submission.selftext is '':
            self._contentBox.insert("1.0", submission.url)
        else:
            self._contentBox.insert("1.0", submission.selftext)
        self.getImage(submission)
        self.setStats(submission)

    def changeSubreddit(self):
        self._bot.changeSubreddit(self._newSub.get())
        self.populateListbox()
