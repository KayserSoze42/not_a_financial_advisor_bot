import json
import os
from datetime import datetime

import matplotlib.pyplot as pyplot
import praw
import pytz
import requests
import yfinance
from imgurpython import ImgurClient
from random import randint


class Ticker:

    def __init__(self, tickerSymbol, user):
        self.user = user
        self.tickerSymbol = tickerSymbol
        self.tickerChange = ""
        self.tickerLastRefresh = ""
        self.tickerOpen = ""
        self.tickerHigh = ""
        self.tickerLow = ""
        self.tickerClose = ""
        self.tickerVolume = ""
        self.tickerAPIData = ""
        self.tickerGraphData = ""
        self.tickerInstance = yfinance.download(self.tickerSymbol, period="1d", prepost=True)

    def updateTicker(self):
        self.tickerAPIData = []
        self.tickerChange = ""

        self.tickerInstance = yfinance.download(self.tickerSymbol, period="1d", prepost=True)

        self.tickerAPIData = self.tickerInstance.values.tolist()
        print(self.tickerInstance)
        self.tickerLastRefresh = self.tickerInstance.iloc[1].name.date()

        self.tickerOpen = self.tickerAPIData[0][0]
        self.tickerClose = self.tickerAPIData[0][3]
        self.tickerHigh = self.tickerAPIData[0][1]
        self.tickerLow = self.tickerAPIData[0][2]
        self.tickerVolume = self.tickerAPIData[0][5]

        self.getChange()

    def getChange(self):
        self.tickerChange = ""
        try:
            data = yfinance.download(self.tickerSymbol, period="5d", prepost=True).values.tolist()
            self.tickerChange = self.calculateChange(data[4][3], data[3][3])
        except:
            print("NAFA ERROR: Unable to update change")

        return self.tickerChange

    def calculateChange(self, current, previous):
        if current == previous:
            return "0%"
        try:
            return str((abs(current - previous) / previous) * 100.0) + "%"
        except ZeroDivisionError:
            return "x%"

    def plotGraphs(self):
        # Plot for 1 day and save as graph1.png
        self.tickerGraphData = yfinance.download(self.tickerSymbol, period="1d", interval="1m")
        self.tickerGraphData.Close.plot(color="green", linestyle="solid")
        self.saveGraph("graph1.png")
        pyplot.cla()

        # Plot for 5 days and save as graph5.png
        self.tickerGraphData = yfinance.download(self.tickerSymbol, period="5d", interval="1m")
        self.tickerGraphData.Close.plot(color="green", linestyle="solid")
        self.saveGraph("graph5.png")
        pyplot.cla()

        # Plot for 1 month and save as graph30.png
        self.tickerGraphData = yfinance.download(self.tickerSymbol, period="1mo", interval="1d")
        self.tickerGraphData.Close.plot(color="green", linestyle="solid")
        self.saveGraph("graph30.png")
        pyplot.cla()

        # Plot for 3 months and save as graph90.png
        self.tickerGraphData = yfinance.download(self.tickerSymbol, period="3mo", interval="1d")
        self.tickerGraphData.Close.plot(color="green", linestyle="solid")
        self.saveGraph("graph90.png")
        pyplot.cla()

        # Plot for 6 months and save as graph180.png
        self.tickerGraphData = yfinance.download(self.tickerSymbol, period="6mo", interval="1d")
        self.tickerGraphData.Close.plot(color="green", linestyle="solid")
        self.saveGraph("graph180.png")
        pyplot.cla()

        # Plot for 1 year and save as graph360.png
        self.tickerGraphData = yfinance.download(self.tickerSymbol, period="1y", interval="1d")
        self.tickerGraphData.Close.plot(color="green", linestyle="solid")
        self.saveGraph("graph360.png")
        pyplot.cla()

    def saveGraph(self, name):
        return pyplot.savefig("graphs/" + name)


class Comment:

    def __init__(self, tickerName, user):
        self.redditInstance = praw.Reddit(
            client_id=user.getClientID(),
            client_secret=user.getClientSecret(),
            user_agent="not_a_financial_advisor_bot",
            username=user.getUsername(),
            password=user.getPassword()
        )

        self.user = user

        self.signatureList = []

        self.imgurInstance = ImgurClient(user.getImgurID(), user.getImgurSecret())
        self.tickerName = tickerName
        self.subreddit = self.redditInstance.subreddit("Superstonk")
        self.dailyThread = self.getDailyThread()

        self.text = []
        self.formattedText = ""

        self.imgurLinks = {}

    def getDailyThread(self):
        for submission in self.subreddit.hot(limit=10):
            if self.tickerName in submission.title and "Daily" in submission.title:
                return submission

    def setSignatureList(self, newList):
        self.signatureList = newList

    def addLine(self, newLine):
        self.text.append(newLine)

    def clearLines(self):
        self.text = ""
        self.formattedText = ""

    def format(self):
        self.formattedText = ""
        self.formattedText += "    ╬══════════════════════  \n    "

        for line in self.text:
            self.formattedText += "║{:^35}".format(line) + "  \n    "

        self.formattedText += "╬══════════════════════  \n    "

    def post(self):

        try:
            self.getDailyThread()
            self.dailyThread.reply(self.formattedText)
        except:
            pass

    def uploadGraphs(self):

        self.imgurLinks = {}

        album = None

        for file in os.listdir(os.getcwd() + "/graphs/"):
            config = {
                'album': album,
                'name': datetime.now().strftime("%Y-%m-%d %I:%M %p"),
                'title': datetime.now().strftime("%Y-%m-%d %I:%M %p"),
                'description': 'Fresh Crayons Out Of The Street'
            }

            image = self.imgurInstance.upload_from_path(os.getcwd() + "/graphs/" + file, config=config, anon=True)

            self.imgurLinks[file] = image["link"]

        self.formattedText += "  \n"
        self.formattedText += 'Crayons: ' + '[1D](' + self.imgurLinks["graph1.png"] + '), ' \
                              + '[5D](' + self.imgurLinks["graph5.png"] + '), ' \
                              + '[1M](' + self.imgurLinks["graph30.png"] + '), ' \
                              + '[3M](' + self.imgurLinks["graph90.png"] + '), ' \
                              + '[6M](' + self.imgurLinks["graph180.png"] + '), ' \
                              + '[1Y](' + self.imgurLinks["graph360.png"] + '), '

        self.formattedText += "  \n ^Beep ^Bop, ^I'm ^a ^bot  \n [go on, git]" + \
                              "(" + self.user.getGithub() + ") " \
                                                            "[or else, join](" + self.user.getSubreddit() + ")  \n  "

        self.formattedText += str(self.signatureList[randint(0, len(self.signatureList) - 1)]) + "  \n"
