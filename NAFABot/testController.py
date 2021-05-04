import os
import time
from datetime import datetime

import pytz
import schedule

from NAFA import Ticker, Comment
from NAFAUser import UserCredentials


def setUpUserInfo():

    try:
        tickerName = os.environ.get("STOCK_NAME")
        userOS = UserCredentials(
            os.environ.get("REDDIT_USERNAME"),
            os.environ.get("REDDIT_PASSWORD"),
            os.environ.get("REDDIT_CLIENTID"),
            os.environ.get("REDDIT_SECRET"),
            os.environ.get("IMGUR_CLIENTID"),
            os.environ.get("IMGUR_SECRET")
        )

        userOS.setGithub(os.environ.get("USER_GITHUB"))
        userOS.setUserSubreddit(os.environ.get("TARGET_SUBREDDIT"))
        userOS.setSubreddit(os.environ.get("USER_SUBREDDIT"))

        mainTicker = Ticker(tickerName, userOS)
        redditComment = Comment(tickerName, userOS)

        print("**\nUSER INFO SET\n**")
        return [mainTicker, redditComment]
    except:
        print("NAFA U - CONTROLLER ERROR: Unable to get User Info, Setting Up Default: NONE")


def init():
    print("Starting up")

    print(datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"))

    instances = setUpUserInfo()

    redditComment = instances[1]
    mainTicker = instances[0]


    redditComment.setSignatureList([
        "^The ^Cake ^Is ^A ^Pie",
        "^Check ^Your ^Posture!",
        "*Tl;dr: 01101000 01101111 01100100 01101100*",
        "^They ^Took ^Er ^Jobs!",
        "^Ceci ^n'est ^pas ^une ^chat",
        "^Tell ^me ^the ^difference ^between ^stupid ^and ^illegal  \n ^and ^I'll ^have ^my ^wife's ^brother ^arrested.",
        "Alexa play Money by Pink Floyd",
        "Alexa play Feel Good Inc. by Gorillaz",
        "Alexa play Lithium by Nirvana",
        "Alexa play When the Levee Breaks by Led Zeppelin"
    ])

    marketUpdate(mainTicker, redditComment)
    schedule.every(5).minutes.do(printUpdate)


def marketUpdate(mainTicker, redditComment):
    # Comment next line if you want to avoid auto posting
    print("Fetching initial data and posting for the first time\n " +
          datetime.now(pytz.timezone("America/New_York")).strftime("%m-%d-%Y %I:%M:%S %p"))
    marketJob(mainTicker, redditComment)
    schedule.every(1).hour.do(marketJob, mainTicker=mainTicker, redditComment=redditComment)


def printUpdate():
    print("Waiting for scheduled update. \nCurrent Time NY:" +
          datetime.now(pytz.timezone("America/New_York")).strftime("%m-%d-%Y %I:%M:%S %p") +
          "\nCurrent Time Local: " +
          datetime.now().strftime("%m-%d-%Y %I:%M:%S %p"))


def marketJob(mainTicker, redditComment):
    mainTicker.updateTicker()

    redditComment.addLine("Current Date and Time:")
    redditComment.addLine(datetime.now(pytz.timezone("America/New_York")).strftime("%Y-%m-%d %I:%M:%S %p"))
    redditComment.addLine("$" + mainTicker.tickerSymbol)
    redditComment.addLine("For Date: " + mainTicker.tickerLastRefresh)
    redditComment.addLine("Close: $" + format(float(mainTicker.tickerClose), '.2f') + " / " + mainTicker.tickerChange)
    redditComment.addLine("Open: $" + format(float(mainTicker.tickerOpen), '.2f'))
    redditComment.addLine(
        "Low / High: $" + format(float(mainTicker.tickerLow), '.2f') + " / $" + format(float(mainTicker.tickerHigh),
                                                                                       '.2f'))
    redditComment.addLine(str("Volume: " + "{:,}".format(int(mainTicker.tickerVolume))))

    mainTicker.plotGraphs()

    redditComment.format()
    redditComment.uploadGraphs()

    print(redditComment.formattedText)

    redditComment.post()


if __name__ == "__main__":
    init()

    while True:
        schedule.run_pending()
        time.sleep(1)
