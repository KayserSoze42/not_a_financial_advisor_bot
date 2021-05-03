import json
import os
from datetime import datetime

import matplotlib.pyplot as pyplot
import praw
import requests
import yfinance
from imgurpython import ImgurClient


class Ticker:

    def __init__(self, tickerSymbol, user):
        self.user = user
        self.tickerSymbol = tickerSymbol
        self.tickerLastRefresh = ""
        self.tickerOpen = ""
        self.tickerHigh = ""
        self.tickerLow = ""
        self.tickerClose = ""
        self.tickerVolume = ""
        self.tickerAPIData = ""
        self.tickerGraphData = ""
        self.tickerURL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=" \
                         + self.tickerSymbol + "&apikey=" + user.getAPIKey()

    def getResponse(self):
        try:
            return json.loads(requests.get(self.tickerURL).content)
        except:
            pass

    def updateTicker(self):
        tickerAPIData = None

        while (tickerAPIData == None):
            tickerAPIData = self.getResponse()

        self.tickerLastRefresh = tickerAPIData["Meta Data"]["3. Last Refreshed"]
        self.tickerOpen = tickerAPIData["Time Series (Daily)"][self.tickerLastRefresh]["1. open"]
        self.tickerHigh = tickerAPIData["Time Series (Daily)"][self.tickerLastRefresh]["2. high"]
        self.tickerLow = tickerAPIData["Time Series (Daily)"][self.tickerLastRefresh]["3. low"]
        self.tickerClose = tickerAPIData["Time Series (Daily)"][self.tickerLastRefresh]["4. close"]
        self.tickerVolume = tickerAPIData["Time Series (Daily)"][self.tickerLastRefresh]["6. volume"]

    def plotGraphs(self):
        # Plot for 1 day and save as graph1.png
        self.tickerGraphData = yfinance.download(self.tickerSymbol, self.tickerLastRefresh)
        self.tickerGraphData.Close.plot(color="green", linestyle="solid")
        self.saveGraph("graph1.png")
        pyplot.cla()

        # Plot for 5 days and save as graph5.png
        self.tickerGraphData = yfinance.download(self.tickerSymbol, period="5d")
        self.tickerGraphData.Close.plot(color="green", linestyle="solid")
        self.saveGraph("graph5.png")
        pyplot.cla()

        # Plot for 1 month and save as graph30.png
        self.tickerGraphData = yfinance.download(self.tickerSymbol, period="1mo")
        self.tickerGraphData.Close.plot(color="green", linestyle="solid")
        self.saveGraph("graph30.png")
        pyplot.cla()

        # Plot for 3 months and save as graph90.png
        self.tickerGraphData = yfinance.download(self.tickerSymbol, period="3mo")
        self.tickerGraphData.Close.plot(color="green", linestyle="solid")
        self.saveGraph("graph90.png")
        pyplot.cla()

        # Plot for 6 months and save as graph180.png
        self.tickerGraphData = yfinance.download(self.tickerSymbol, period="6mo")
        self.tickerGraphData.Close.plot(color="green", linestyle="solid")
        self.saveGraph("graph180.png")
        pyplot.cla()

        # Plot for 1 year and save as graph360.png
        self.tickerGraphData = yfinance.download(self.tickerSymbol, period="1y")
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

    def addLine(self, newLine):
        self.text.append(newLine)

    def clearLines(self):
        self.text = ""
        self.formattedText = ""

    def format(self):
        self.formattedText = ""
        self.formattedText += "    ╬══════════════════════  \n    "

        for line in self.text:
            self.formattedText += "║{:^28}".format(line) + "  \n    "

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

        self.formattedText += "  \n ^Beep Bop, I'm a bot  \n [go on, git]" \
                              "(https://github.com/KayserSoze42/not_a_financial_advisor_bot) " \
                              "[or else, join](https://www.reddit.com/r/not_an_advisor_bot/)  \n  "
