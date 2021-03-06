import os
import time
from datetime import datetime, timedelta

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

        userOS.setUserGithub(os.environ.get("USER_GITHUB"))
        userOS.setUserSubreddit(os.environ.get("USER_SUBREDDIT"))
        userOS.setTargetSubreddit(os.environ.get("TARGET_SUBREDDIT"))


        mainTicker = Ticker(tickerName, userOS)
        redditComment = Comment(tickerName, userOS)

        startMarketTime = os.environ.get("BOT_START")
        intervalJobTime = int(os.environ.get("BOT_INTERVAL"))

        print("**\nUSER INFO SET\n**")
        return [mainTicker, redditComment, startMarketTime, intervalJobTime]
    except:
        print("NAFA U - CONTROLLER ERROR: Unable to get User Info, Setting Up Default: NONE")


def init():
    print("Starting up")

    print(datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"))

    instances = setUpUserInfo()

    redditComment = instances[1]
    mainTicker = instances[0]
    startMarketTime = instances[2]
    intervalJobTime = instances[3]

    redditComment.setSignatureList([
        "^The ^Cake ^Is ^A ^Pie",
        "^HOLY ^MOLY",
        "^74 ^6f ^20 ^74 ^68 ^65 ^20 ^6d ^6f ^6f ^6e ^21",
        "^Good ^Morning ^Everyone!",
        "^Is ^mayonnaise ^an ^instrument?",
        "^All ^your ^gains ^are ^belong ^to ^us",
        "^Much ^wow",
        "^Donde, ^está, ^la ^biblioteca. ^Me ^llamo ^T-Bone, ^la ^araña ^discoteca",
        "^stonks",
        "^Check ^Your ^Posture!",
        "^Tl;dr: ^01101000 ^01101111 ^01100100 ^01101100",
        "^Ceci ^n'est ^pas ^une ^chat",
        "^Is ^This ^The ^Way?",
        "^Tell ^me ^the ^difference ^between ^stupid ^and ^illegal ^and ^I'll ^have ^my ^wife's ^brother ^arrested.",
        "^I ^came ^here ^to ^chew ^bubblegum ^and ^post ^data, ^but ^I'm ^all ^out ^of ^bubblegum",
        "Alexa play Money by Pink Floyd",
        "Alexa play The Blue Wrath by I Monster",
        "Alexa play The Greenback Boogie by Ima Robot",
        "Alexa play Feel Good Inc by Gorillaz",
        "Alexa play Lithium by Nirvana",
        "Alexa play When the Levee Breaks by Led Zeppelin",
        "Alexa play Tubthumping by Chumbawamba",
        "Alexa play Time Is On My Side by The Rolling Stones"
    ])

    schedule.every().day.at(startMarketTime).do(marketUpdate, mainTicker=mainTicker, redditComment=redditComment, startMarketTime=startMarketTime, intervalJobTime=intervalJobTime)

    print("Scheduled Successfully\n")
    printNextPostDate(startTime=startMarketTime)


def marketUpdate(mainTicker, redditComment, startMarketTime, intervalJobTime):
    # Comment next line if you want to avoid auto posting
    print("Fetching initial data and posting for the first time\nLocal Time:\n" +
          datetime.now().strftime("%Y-%m-%d %I:%M:%S %p") + "\nUS Time:\n" +
          datetime.now(pytz.timezone("America/New_York")).strftime("%m-%d-%Y %I:%M:%S %p"))
    marketJob(mainTicker, redditComment, intervalJobTime)

    schedule.every(intervalJobTime).minutes.do(marketJob, mainTicker=mainTicker, redditComment=redditComment, intervalJobTime=intervalJobTime)
    schedule.every(5).minutes.do(printUpdate, mainTicker=mainTicker, redditComment=redditComment, startMarketTime=startMarketTime, intervalJobTime=intervalJobTime)


def printUpdate(mainTicker, redditComment, startMarketTime, intervalJobTime):
    currentDateUS = datetime.now(pytz.timezone("America/New_York"))

    print("\nWaiting for scheduled update. \nCurrent Time NY: " +
          datetime.now(pytz.timezone("America/New_York")).strftime("%m-%d-%Y %I:%M:%S %p") +
          "\nCurrent Time Local: " +
          datetime.now().strftime("%m-%d-%Y %I:%M:%S %p"))

    if int(currentDateUS.strftime("%I")) >= 4 and int(currentDateUS.strftime("%M")) >= 30 and currentDateUS.strftime("%p") == "PM":

        print("\nMarket Closed, cancelling all jobs for today")
        printNextPostDate(startTime=startMarketTime)
        schedule.clear()
        schedule.every().day.at(startMarketTime).do(marketUpdate, mainTicker=mainTicker, redditComment=redditComment,
                                                    startMarketTime=startMarketTime, intervalJobTime=intervalJobTime)


def marketJob(mainTicker, redditComment, intervalJobTime):
    print("\nStarting Market Job\n\nUpdating Ticker Data")

    mainTicker.updateTicker()

    print("\n***\nUPDATED\n***\n")

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

    print("\nPlotting Graphs\n")

    mainTicker.plotGraphs()

    print("\n***\nDONE\n***\n")

    redditComment.format()
    redditComment.uploadGraphs()

    print("\nFinishing Work And Printing\n")

    print(redditComment.formattedText)

    redditComment.post()

    print("\n***\nDONE\n***\n")

    printNextPostDate(interval=intervalJobTime)


def printNextPostDate(startTime=None, interval=30):

    currentDate = datetime.now()
    currentDateUS = datetime.now(pytz.timezone("America/New_York"))

    if int(currentDateUS.strftime("%I")) >= 4 and int(currentDateUS.strftime("%M")) >= 30 \
            and currentDateUS.strftime("%p") == "PM":
        nextPostDate = currentDate + timedelta(days=1)
        nextPostDate = nextPostDate.strftime("%Y-%m-%d ") + datetime.strptime(startTime, "%H:%M").strftime("%I:%M:%S %p")
        print("NEXT POST:\n" + nextPostDate + "\n")

    elif startTime is not None:
        nextPostDate = currentDate.strftime("%Y-%m-%d ") + datetime.strptime(startTime, "%H:%M").strftime("%I:%M:%S %p")
        print("NEXT POST:\n" + nextPostDate + "\n")

    else:
        nextPostDate = currentDate + timedelta(minutes=interval)
        nextPostDate = nextPostDate.strftime("%Y-%m-%d %I:%M:%S %p")
        print("NEXT POST:\n" + nextPostDate + "\n")


if __name__ == "__main__":
    init()

    while True:
        schedule.run_pending()
        time.sleep(1)
