from bs4 import BeautifulSoup
from urllib.request import urlopen
import datetime
import telegram
import schedule
import time

TOKEN_TELEGRAM = '335844830:AAFHubomXjxZD4DlVsW9ql5zHLt9f1Cutyo' #HN_TG_BOT
bot = telegram.Bot( TOKEN_TELEGRAM )

try:
    update_id = bot.getUpdates()[0].update_id
except IndexError:
	update_id = None
chat_id = 31923577

def getHNentries():
	try:
		for year in range(2010, int( datetime.datetime.now().strftime("%Y") ) + 1 ): # + 1 including this year
			text = ""
			date = datetime.datetime.now() - datetime.timedelta( days = 1 )
			url = 'http://www.daemonology.net/hn-daily/{}-{}.html'.format( year, date.strftime("%m-%d") )
			print(url)
			try:
				html = urlopen( url ).read()
			except Exception as e:
				continue
			bsObj = BeautifulSoup(html,"html.parser").findAll("div",{"class":"content"})[0].findAll("span",{"class":"storylink"})
			for item in bsObj:
				text = text + '<b>{}</b> (<a href="{}">{}</a>)\n\n'.format(item.text,item.a.attrs["href"],"link")
			text = "<b>" + date.strftime("%d/%m/") + str(year) + "</b>\n" + "\n" + text
			bot.sendMessage(parse_mode = "Html", text = text, chat_id = chat_id, disable_web_page_preview = True)
	except Exception as e:
		print(e)

schedule.every().day.at("2:20").do( getHNentries )

while True:
    schedule.run_pending()
    time.sleep(1801)

