from os import system
from time import sleep, time
from stats_main import *

start = time()  # Start logging time

system("rm -Rf ../output/*")  # Clear old logs

scrape_list = ['EliteDangerous', 'Funny']

for sub in scrape_list:
    print "SCRAPING : /r/%s" % sub
    sleep(1)
    system("cd ../../../;\
            scrapy crawl reddits -a current_subreddit=" + sub)

end = time()

print "Scraped %s page(s).\nTime: %s seconds" % (len(scrape_list), str(end-start)[0:5])

print stats_master(json_list=jsondirectory, target_key=('text'), search_words=['league'])