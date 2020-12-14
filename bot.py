import twint
import time
import apscheduler
from apscheduler.schedulers.background import BackgroundScheduler
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import date, timedelta

#Bot configuration
# Create the Updater and pass it your bot's token.
updater = Updater(token='')

# Start the Bot
updater.start_polling()

def tweetscrap():
    config = twint.Config()
    config.Search = "#bugbountytip OR #bugbounty OR #bugbountytips"
    config.Lang = "en"
    config.Limit = 10
    config.Min_likes = 100
    config.Filter_retweets = True
    config.Hide_output = True
    config.Store_object = True
    config.Popular_tweets = True
    config.Since = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')+" 00:00:00"
    config.Until = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')+" 23:59:00"
    tipsofday = "#BugBountyTips of the Day\n\r"
    twint.run.Search(config)
    tweets = twint.output.tweets_list
    if len(twint.output.tweets_list) != 0:
        for tweet in tweets:
            if tweet != tweets[-1]:
                tipsofday = f"{tipsofday}{tweet.tweet}\n\r---\n\r"
            else: 
                tipsofday = f"{tipsofday}{tweet.tweet}"
        updater.bot.sendMessage(chat_id='@bhhub', text=tipsofday)
    twint.output.tweets_list.clear()

scheduler = BackgroundScheduler({'apscheduler.timezone': 'UTC'})
scheduler.add_job(tweetscrap, 'cron', hour='13', minute='37')
scheduler.start()
while True:
    time.sleep(1)