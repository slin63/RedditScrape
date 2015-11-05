# Contains main functions for parsing json data collected by Scrapy
from time import localtime
from statfunctions import *


def stats_master(json_list, target_key, search_words):
    """Given a list of json files, opens them from the output directory
    and reads them using stats_slave. Returns dictionary with results for
    each individual subreddit and a tuple with sum results."""
    index = 0
    dic = {}

    for jsonfile in json_list:
        open_file = os.path.join(fileDir, '../output/' + jsonfile)
        results = stats_slave(json_tup=json_to_tuple(open_file), t=target_key, s=search_words)
        dic[jsonfile] = (results[0], results[1], results[2])
        index += 1

    t = localtime()
    t_string = "%s/%s/%s %s:%s:%s" % (t[1], t[2], t[0], t[3], t[4], t[5])

    return t_string, dic


def stats_slave(json_tup, t, s):
    """Working component of stats_master, parses json files for
    interesting information and passes it off to stats_master."""
    stat_dict = search_json_string(json_tup, t, s)
    json_length = len(json_tup)
    number_comments_hits = len(stat_dict)
    number_of_hits = sum(stat_dict.values())

    return json_length, number_comments_hits, number_of_hits


