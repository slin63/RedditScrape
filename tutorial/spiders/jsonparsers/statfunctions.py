import json
from string import find
import os

fileDir = os.path.dirname(os.path.realpath('__file__'))


def json_to_tuple(filename):
    """Opens a file formatted in .json and indexes .json strings into an empty tuple.
    I think the tuple will make processing of large quantities of items faster but who knows?"""
    filehandle = open(filename)
    json_tup = ()
    for line in filehandle:
        json_tup += ((json.loads(line)),)  # json.loads() converts json string to workable dict
    filehandle.close()
    return json_tup


def search_string(string, key):
    """Iteratively searches through target string for given key
    and returns number of matches between key and target."""
    indices = []
    string_copy = string.lower()
    while find(string_copy,key) != -1:
        indices.append(find(string_copy,key))
        string_copy = RepNSlice(string_copy,find(string_copy,key),key)
    return len(indices)


def RepNSlice(st, index, key):
    """Helper function to search_string.
    Takes a given non-mutable type string and converts
    it into a mutable list. Modifies a single value to prevent
    its rediscovery via string.find() but preserves index values."""
    l = list(st)
    l[index:index+len(key)] = '!'*len(key)
    return ''.join(l)


def search_json_string(json_tup, target_key, search_words):  # This is really gross and needs to be changed or replaced
    """Given a tuple filled with json dicts, a key under which we will search, and
    a list of words to look for, returns a dict of form {url: # of instances of words}
    Note: When searching for short words like 'a' or 'he', put whitespaces around them
    e.g. ' a ', ' he ', so that portions of other words are not confused for the actual word."""
    link_dict = {}
    for jsons in json_tup:
        for word in search_words:  # Initializes dictionary entrances
            count = search_string(jsons[target_key][0], word)
            if count:
                try:
                    link_dict[jsons['hyperlink'][0]] = 0
                except KeyError:
                    link_dict[jsons['url'][0]] = 0

        for word in search_words:  # Populates dictionary entrances with counts
            count = search_string(jsons[target_key][0], word)
            if count:
                try:
                    link_dict[jsons['hyperlink'][0]] += count
                except KeyError:
                    link_dict[jsons['url'][0]] += count
    return link_dict


def separate_stats(stats_dic):  # Just use tuple pairs . . .
    """Splits a dictionary containing thread and comment
    info into two separate tuple-tuple combinations."""
    comment_dic = ()
    thread_dic = ()

    for e in stats_dic:
        # print e
        if e[-5] == 'C':
            comment_dic += ((e[0:-5], stats_dic[e]),)
        elif e[-5] == 'T':
            thread_dic += ((e[0:-5], stats_dic[e]),)

    return sorted(comment_dic), sorted(thread_dic)
