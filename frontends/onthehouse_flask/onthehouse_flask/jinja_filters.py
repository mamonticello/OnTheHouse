'''
This file provides functions which can be called from within Jinja templates.
Instead of `length(items)`, filter calls look like `items|length`
'''
import datetime

def split_paragraphs(text):
    paragraphs = text.strip().split('\n\n')
    paragraphs = [p.replace('\n', ' ') for p in paragraphs]
    return paragraphs

def unix_to_human(timestamp):
    then = datetime.datetime.utcfromtimestamp(timestamp)
    then = then.strftime('%b %d, %Y')
    return then
