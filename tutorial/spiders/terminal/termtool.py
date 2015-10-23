from os import system
from time import sleep

system("rm -Rf ../output/*")

scrape_list = ['AskReddit', 'EliteDangerous', 'Funny']

for sub in scrape_list:
    print "SCRAPING : %s" % sub
    sleep(1)
    system("cd ../../../; scrapy crawl reddits -a current_subreddit="+sub)
    sleep(1)