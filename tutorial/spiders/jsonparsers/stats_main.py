# Contains main functions for parsing json data collected by Scrapy

from statfunctions import *
fileDir = os.path.dirname(os.path.realpath('__file__'))
jsondirectory = os.listdir("../output")


def stats_master(json_list, target_key, search_words):
    """Given a list of json files, opens them from the output directory
    and reads them using stats_slave. Returns dictionary with results for
    each individual subreddit and a tuple with sum results."""
    index = 0
    posts = 0  # Total posts read
    comment_hits = 0  # Individual text posts containing words
    number_hits = 0  # Number of times words are mentioned total
    dic = {}

    for jsonfile in json_list:
        open_file = os.path.join(fileDir, '../output/' + jsonfile)
        results = stats_slave(json_tup=json_to_tuple(open_file), t=target_key, s=search_words)
        posts += results[0]
        comment_hits += results[1]
        number_hits += results[2]
        dic[jsonfile] = (results[0], results[1], results[2])
        index += 1

    return dic, (posts, comment_hits, number_hits)


def stats_slave(json_tup, t, s):
    """Working component of stats_master, parses json files for
    interesting information and passes it off to stats_master."""
    # print "Scraping: %s \n" % jsonfile + "-" * 80
    stat_dict = search_json_string(json_tup, t, s)
    json_length = len(json_tup)
    number_comments_hits = len(stat_dict)
    number_of_hits = sum(stat_dict.values())

    # print "Total posts: %s\n%% of posts containing words in search_words: %s%%\nTotal number of hits: %s"% (json_length, str((100.0*number_comments_hits)/json_length)[0:4], number_of_hits)

    # print stat_dict.keys()

    return json_length, number_comments_hits, number_of_hits


print stats_master(json_list=jsondirectory, target_key=('text'), search_words=['league'])