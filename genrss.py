#!/usr/bin/python
from requests import get
from BeautifulSoup import BeautifulSoup as bs
from soupselect import select
from PyRSS2Gen import RSS2, RSSItem, _opt_element, IntElement, _element, Enclosure
from datetime import datetime

class FeedItem(RSSItem):
    media_content = None
    
    def __init__(self, **kwargs):
        self.media_content = kwargs['media_content']
        del kwargs['media_content']
        RSSItem.__init__(self, **kwargs)

    def publish_extensions(self, handler):
        _opt_element(handler, "media:content", self.media_content)
        _opt_element(handler, "itunes:explicit", "no")
        _opt_element(handler, "itunes:subtitle", "butt")
        _opt_element(handler, "itunes:author", "Virginia Foundation for the Humanities")
        _opt_element(handler, "itunes:summary", "butt")


class Media:
    def __init__(self, url):
        self.url = url
    def publish(self, handler):
        handler.startElement('media:content', { 'url': self.url })
        handler.endElement('media:content')


months = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split(' ')

b = bs(get('http://backstoryradio.org/archives/').text)
monthlinks = [a['href'] for a in b('a') if a.text in months]

def links(b, sel):
    return [a['href'] for a in select(b, sel)]

def get_mp3s():
    mp3s = []
    for m in monthlinks:
        print 'Fetching', m
        b = bs(get(m).text)
        for post in select(b, 'h3.posttitle a'):
            title = post.text
            href = post['href']
            for mp3 in links(bs(get(href).text), 'a[title=Download]'):
                mp3s.append((title, mp3))
    return mp3s


def getsize(url):
    return 12345


rss = RSS2(
    title = "Backstory Archive",
    link = "backstoryradio.org",
    description = "back episodes of backstory",
    lastBuildDate = datetime.now(),
    items = [
        FeedItem(
            title = title,
            media_content = Media(url),
            link = url,
            guid = url,
            comments = 'butt',
            author = 'mcfunley@gmail.com',
            pubDate = datetime.now(),
            enclosure = Enclosure(url, getsize(url), "audio/mpeg"),
            )

        for title, url in get_mp3s()
        ]
    )

rss.write_xml(open('backstory.xml', 'w'))


