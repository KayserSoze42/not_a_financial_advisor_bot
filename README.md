# not_a_financial_advisor_bot
Bot that fetches recent ticker info.  It formats the data and posts it on a thread during market hours (+ pre and post). Also makes bad jokes 

To start the bot script use the Virtual Environment and start the testController.py
It requires next Environment Variables to be set in order to work:
                      
              - REDDIT_USERNAME, REDDIT_PASSWORD, REDDIT_CLIENTID, REDDIT_SECRET, IMGUR_CLIENTID, IMGUR_SECRET, STOCK_NAME, USER_GITHUB, USER_SUBREDDIT

Currently it's WIP, but the main idea is to keep NAFA modules seperate from the Controllers so it can be re-used for other subreddits, threads and tickers
