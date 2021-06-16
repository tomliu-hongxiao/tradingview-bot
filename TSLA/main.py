import datetime
import time


from bot import Bot

# *************    交易 对象    ***************#

symbol = "TSLA"

# *******************************************#

current_time = datetime.datetime.now().replace(microsecond=0)
bot_start_time = current_time.replace(hour=9, minute=50, second=0, microsecond=0)
time_dif = bot_start_time - current_time
if bot_start_time > current_time:
    print("bot will start at 9 : 50")
    time.sleep(time_dif.total_seconds())

bot = Bot(symbol)
