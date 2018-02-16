'''
This file provides functions which can be called from within Jinja templates.
Instead of `length(items)`, filter calls look like `items|length`
'''
def split_paragraphs(text):
    paragraphs = text.strip().split('\n\n')
    paragraphs = [p.replace('\n', ' ') for p in paragraphs]
    return paragraphs
