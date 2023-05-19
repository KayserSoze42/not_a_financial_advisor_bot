# not_a_financial_advisor_bot
Bot that fetches recent ticker info.  It formats the data and posts it on a thread during market hours. Also makes bad jokes 

To start the bot script use the Virtual Environment and start the testController.py

It requires next Environment Variables to be set in order to work:
                      
    REDDIT_USERNAME, REDDIT_PASSWORD, REDDIT_CLIENTID, REDDIT_SECRET, IMGUR_CLIENTID, IMGUR_SECRET, STOCK_NAME, USER_GITHUB, USER_SUBREDDIT, TARGET_SUBREDDIT, BOT_START, BOT_INTERVAL

Currently it's WIP, but the main idea is to keep NAFA modules seperate from the Controllers so it can be re-used for other subreddits, threads and tickers

If you're planning on using the script with Docker, my recommendation is to create an env.list file with all of the Environment Variables, where each row equals to KEY=VALUE (without quotation marks) and then running the container with option _--env-file env.list_

Example of NAFA modules usage:

    First initialize the User Object:
                              
                              UserCredentials(
                                  Username for the Reddit Account,
                                  Password for the Reddit Account,
                                  Reddit APP Client ID,
                                  Reddit APP Client Secret,
                                  Imgur APP Client ID,
                                  Imgur APP Client Secret
                              )
                              
                              UserCredentials.setUserGithub(URL for the home Github page)
                              UserCredentials.setUserSubreddit(URL for the home Subreddit)
                              UserCredentials.setTargetSubreddit(Name of the subreddit with the Daily Thread)
                              
    Then initialize the Ticker and Comment Objects:
                              
                              Ticker(
                                  Ticker Symbol,
                                  UserCredentials Object
                              )
                              
                              Comment(
                                  Ticker Symbol,
                                  UserCredentials Object
                              )
                              
                              Comment.setSignatureList(List with signatures to be added at the bottom of the post)
                              
    To update the data and post:
    
                              Ticker.updateTicker()                   - Fetches recent data from yfinance
                              
                              Ticker.tickerOpen 
                              Ticker.tickerClose
                              Ticker.tickerHigh
                              Ticker.tickerLow                        - Access the Ticker Object data
                              Ticker.tickerVolume
                              Ticker.tickerLastRefresh
                              Ticker.getChange()
                              
                              Comment.addLine(newLine : string)       - Add new line of text to the comment (inside the Box, to add bellow set signatures)
                              
                              Ticker.plotGraphs()                     - Plot 1d,5d,1m,3m,6m,1y graphs using matplotlib.pyplot
                              
                              Comment.format()                        - Takes all of the lines added and formats them for the body of the box
                              
                              Comment.uploadGraphs()                  - Uploads all of the .png graphs from the /graphs directory and formats the signature(2bf) 
                              
                              Comment.post()                          - Posts the formatted text on the Daily Thread of the TARGET_SUBRREDIT
                              
                              Comment.formattedText                   - To access the comment text
