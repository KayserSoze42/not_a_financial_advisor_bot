# not_a_financial_advisor_bot
Bot that fetches recent ticker info.  It formats the data and posts it on a thread during market hours. Also makes bad jokes 

**-----BEGIN' UPDATE-----** 

_With the current state of the "game", I feel a need to give this monster a proper semi-epitaph._

_I lack the experience to feel the confidence and need to share my thoughts on the actions, so I'll do what I do best. Make jokes and roast my reasonings._

_It was just a quickly put together memeMachine, made to spread data and joy, and I am more than thankful for all of the parties involved (especially "imports" behind scenes) to make such a silly thing possible._

_I was able to (ab)use some math and plot some graphs, all while keeping in trend with the latest memez._

_grep bless Python, the best of the worst and the worst of the best._

_The community's movement is another thing I'm no comment, since investing is yet another abstract thing for me._

_I am happy for the lolz and this is my reasoning:_

_Monty Python may have introduced me to Python, but Darwin and Dawkins provided amemeunition._

_P.S. You can see some [examples](https://www.reddit.com/r/Superstonk/comments/n9rsxg/comment/gxrmj3t/?utm_source=share&utm_medium=web2x&context=3) and its' evolution on my Reddit profile, which shares the name with my GitHub, oh what a reveal._

_P.P.S. I would like to use this oportunity to also state that my other handle, OxieMoron, is in no way, shape or form affiliated with a certain furry handle/persona I have discovered on the first page of a Google search.. To think what truths second page actually hides._

_I'm not judging, but I keep my rule69.zip hidden in a jpeg, where it belongs._

**-----END UPDATE-----**

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
