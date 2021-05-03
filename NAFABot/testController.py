import os
import time
from datetime import datetime

import pytz
import schedule

from NAFA import Ticker, Comment
from NAFAUser import UserCredentials

tickerName = os.environ.get("STOCK_NAME")
userOS = UserCredentials(
    os.environ.get("REDDIT_USERNAME"),
    os.environ.get("REDDIT_PASSWORD"),
    os.environ.get("REDDIT_CLIENTID"),
    os.environ.get("REDDIT_SECRET"),
    os.environ.get("IMGUR_CLIENTID"),
    os.environ.get("IMGUR_SECRET")
)

mainTicker = Ticker(tickerName, userOS)
redditComment = Comment(tickerName, userOS)


def init():
    print("Starting up")

    print(datetime.now().strftime("%Y-%m-%d %I:%M:%S: %p"))

    mainLoop()


def mainLoop():
    schedule.every().day.at("15:30").do(marketUpdate)


def marketUpdate():
    schedule.every(30).minutes.do(marketJob)


def marketJob():
    mainTicker.updateTicker()

    redditComment.addLine("Current Date and Time:")
    redditComment.addLine(datetime.now(pytz.timezone("America/New_York")).strftime("%m-%d-%Y %I:%M:%S %p"))
    redditComment.addLine("$" + mainTicker.tickerSymbol)
    redditComment.addLine("For Date: " + mainTicker.tickerLastRefresh)
    redditComment.addLine("Close: $" + str(mainTicker.tickerClose))
    redditComment.addLine("Open: $" + str(mainTicker.tickerOpen))
    redditComment.addLine("Low / High: $" + format(float(mainTicker.tickerLow), '{.4f}') + " / $" +
                          format(float(mainTicker.tickerHigh), '{.4f}'))
    redditComment.addLine("Volume:" + "{:,}".format(int(mainTicker.tickerVolume)))

    mainTicker.plotGraphs()

    redditComment.format()
    redditComment.uploadGraphs()

    print(redditComment.formattedText)

    redditComment.post()


if __name__ == "__main__":

    init()

    # Comment next line if you want to avoid auto posting
    print("Fetching initial data and posting for the first time\n " +
          datetime.now(pytz.timezone("America/New_York")).strftime("%m-%d-%Y %I:%M:%S %p"))
    marketJob()

    while True:
        schedule.run_pending()
        time.sleep(1)
