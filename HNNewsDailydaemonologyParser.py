from bs4 import BeautifulSoup
from urllib.request import urlopen
import datetime
import telegram
import time
import os
from telegram.ext import *

TOKEN_TELEGRAM = os.environ['TOKEN_TELEGRAM'] #HN_TG_BOT
HOUR_I_WANNA_GET_MESSAGE = int( os.environ['HOUR_I_WANNA_GET_MESSAGE'] )
MINUTES_I_WANNA_GET_MESSAGE = int( os.environ['MINUTE_I_WANNA_GET_MESSAGE'] )
chat_id = int( os.environ['chat_id'] )

def start( bot, update ):
	bot.sendMessage("Successfully subscribed.\nYou will get news every day at {}:{}.\n\nHave fun!".format( HOUR_I_WANNA_GET_MESSAGE, MINUTES_I_WANNA_GET_MESSAGE ))
	
def getHNentries( bot, job ):
	try:
		for year in range(2010, int( datetime.datetime.now().strftime("%Y") ) + 1 ): # + 1 including this year
			text = ""
			date = datetime.datetime.now() - datetime.timedelta( days = 1 )
			url = 'http://www.daemonology.net/hn-daily/{}-{}.html'.format( year, date.strftime("%m-%d") )
			#print(url)
			try:
				html = urlopen( url ).read()
			except Exception as e:
				continue
			bsObj = BeautifulSoup(html,"html.parser").findAll("div",{"class":"content"})[0].findAll("span",{"class":"storylink"})
			bsObjComment = BeautifulSoup(html,"html.parser").findAll("div",{"class":"content"})[0].findAll("span",{"class":"commentlink"})
			for i in range( len(bsObj) ):
				text = text + '<b>{}</b>\n<a href="{}">{}</a>     <a href="{}">{}</a>\n\n'.format(bsObj[i].text, bsObj[i].a.attrs["href"],"[article]", bsObjComment[i].a.attrs["href"] ,"(comments)")
			text = "<b>" + date.strftime("%d/%m/") + str(year) + "</b>\n" + "\n" + text
			bot.sendMessage(parse_mode = "Html", text = text, chat_id = chat_id, disable_web_page_preview = True)
	except Exception as e:
		print(e)

updater = Updater(TOKEN_TELEGRAM) 
dp = updater.dispatcher
updater.dispatcher.add_handler(CommandHandler('start', start))

j = updater.job_queue

utc_offset_heroku = time.localtime().tm_gmtoff / 3600
hour = HOUR_I_WANNA_GET_MESSAGE + ( int(utc_offset_heroku) - 2 ) # 2 is my offset
time2 = datetime.time(hour ,MINUTES_I_WANNA_GET_MESSAGE)

j.run_daily(getHNentries, time2 )

updater.start_polling()
updater.idle()
