import praw
from praw import *
from PIL import Image, ImageTk, ImageOps
from io import BytesIO
import requests

from cfg import *

TITLE_LIMIT = 25


class Redditbot():
    def __init__(self):
        self._reddit = self.login()
        self.subreddit = self._reddit.subreddit('all')
        self._submission = None
        self._comment = None

    def login(self):
        r = Reddit(username=USER, password=PASSWORD, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                   user_agent='testbot (by /u/itsthenewdx2')
        r.user.me()
        return r

    def getPostImage(self, sub):
        try:
            URL = sub.preview['images'][0]['source']['url']
            response = requests.get(URL)
            img = ImageTk.PhotoImage(ImageOps.fit(Image.open(BytesIO(response.content)), (256, 256)))
            return img
        except AttributeError:
            return None

    def getSubmissionList(self):
        submissionList = []
        for submission in self.subreddit.top('all'):
            submissionList.append(submission)
        return submissionList

    def getCommentList(self, submission):
        pass
        # To be implemented in later versions


    def changeSubreddit(self, newsubreddit):
        self._subreddit = newsubreddit
