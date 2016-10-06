# Script that runs spiders in succession and statistics functions

# Stat tool to graph average words per post, most commonly used words in subreddit, etc
# maybe a tool to be able to graph previous scrapes in log.jl

from time import sleep, time
from stats_main import *
from plotter import *
from json import dumps
log = os.path.relpath("../log/log.jl")


def main(scrape_list, target_key, search_words):
    run_spider(scrape_list)
    get_stats(target_key, search_words)

    return 0


def run_spider(scrape_list):
    """Launches the scrapy spider to search the given subreddits in
    scrape_list."""
    start = time()  # Start logging time
    os.system("rm -Rf ../output/*")  # Clear old logs

    for sub in scrape_list:
        print "SCRAPING : /r/%s" % sub
        sleep(1)
        os.system("cd ../../../;\
                scrapy crawl reddits -a current_subreddit=" + sub)
    end = time()

    print "Scraped %s page(s):\n\tTime: %s seconds.\n\tAverage time per page: %s seconds" % \
          (len(scrape_list), str(end-start)[0:5], str((end-start)/len(scrape_list))[0:5])

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

    # separate_stats(stats[1])

    plot(stats[1])

    return 0


tech_list = [
    'space','cars','phones','software','program','computer',
    'screen','keyboard','code','wireless','gadget','wifi','connection','release'
]

main(
     scrape_list=['elitedangerous', 'uiuc', 'askreddit', 'askscience'],
     target_key='text',
     search_words=['fusarium', 'ships', 'combat', 'depression']
)
