# Script that runs spiders in succession and statistics functions

from os import system, path
from time import sleep, time
from stats_main import *
from plotter import *
from json import dumps
log = path.relpath("../log/log.jl")


def run_spider(scrape_list):
    """Launches the scrapy spider to search the given subreddits in
    scrape_list."""
    start = time()  # Start logging time
    system("rm -Rf ../output/*")  # Clear old logs

    for sub in scrape_list:
        print "SCRAPING : /r/%s" % sub
        sleep(1)
        system("cd ../../../;\
                scrapy crawl reddits -a current_subreddit=" + sub)
    end = time()

    print "Scraped %s page(s).\nTime: %s seconds" % (len(scrape_list), str(end-start)[0:5])

    return 0


def get_stats(target_key, search_words):
    """Parses information from .json files compiled by run_spider
    and saves collected data to log.jl."""
    jsondirectory = os.listdir("../output")  # List containing all files inside given directory

    stats = stats_master(jsondirectory, target_key, search_words)

    logs = open(log, 'ab')
    line = dumps(stats) + "\n"
    logs.write(line)
    logs.close()

    plot(stats[1])

    return 0


# run_spider(['dwarffortress','uiuc','pathofexile','EliteDangerous','Funny','iama'])
get_stats(target_key='text', search_words=['dog','dwarf','space','hate','chair','class','savings'])