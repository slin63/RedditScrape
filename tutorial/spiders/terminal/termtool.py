import os
# os.system("ls")
# os.system("cd ..")
os.system("rm -Rf ../output/*")
os.system("scrapy crawl reddits -a current_subreddit='AskReddit'")
