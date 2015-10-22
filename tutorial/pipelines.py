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
file_placeholder = path.relpath("tutorial/spiders/output/foo.jl")


class RedditPipeline(object):
    def process_item(self, item, spider):
        item['text'] = clean_textlist(item['text'])
        if (item['url'])[0][0] == "/":
            item['url'][0] = "https://www.reddit.com" + item['url'][0]
        if item['votes']:
            item['votes'] = clean_votes(item['votes'])
        return item


class JsonWriterPipeline(object):
    def __init__(self):
        self.thread_file = open(file_path_threads, 'wb')       # Refers to generated paths above
        self.comment_file = open(file_path_comments, 'wb')

    def process_item(self, item, spider):
        if item['type'][0] == 'THREAD':
            line = dumps(dict(item)) + "\n"
            self.thread_file.write(line)
        elif item['type'][0] == 'COMMENT':
            line = dumps(dict(item)) + "\n"
            self.comment_file.write(line)
        return item


class ContentSearchPipeline(object):  # Consider graphing results with matlab
    def __init__(self):
        self.file_placeholder = open(file_placeholder, 'wb')

    def process_item(self, item, spider):
        if int(item['votes'][0]) > 2000:
            line = dumps(dict(item)) + "\n"
            self.file_placeholder.write(line)
        return item
