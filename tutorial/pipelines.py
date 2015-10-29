# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES in settings.py
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from tutorial.spiders.filters import clean_textlist, clean_votes
from json import dumps
from os import path

file_path_threads = path.relpath("tutorial/spiders/output/threads.jl")  # Uses .os module to get relative paths to /output
file_path_comments = path.relpath("tutorial/spiders/output/comments.jl")


class RedditPipeline(object):
    def process_item(self, item, spider):
        item['text'] = clean_textlist(item['text'])
        if (item['url'])[0][0] == "/":
            item['url'][0] = "https://www.reddit.com" + item['url'][0]
        if item['votes']:
            item['votes'] = clean_votes(item['votes'])
        return item


class JsonWriterPipeline(object):
    def process_item(self, item, spider):
        thread_file = open(path.relpath("tutorial/spiders/output/"+item['sub']+"TH.jl"), 'ab')
        comment_file = open(path.relpath("tutorial/spiders/output/"+item['sub']+"CO.jl"), 'ab')

        if item['type'][0] == 'THREAD':
            line = dumps(dict(item)) + "\n"
            thread_file.write(line)
        elif item['type'][0] == 'COMMENT':
            line = dumps(dict(item)) + "\n"
            comment_file.write(line)
        return item

