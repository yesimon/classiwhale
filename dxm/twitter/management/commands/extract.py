import itertools
import re
import string
import sys
from urlparse import urlparse

from HTMLParser import HTMLParseError

from BeautifulSoup import BeautifulStoneSoup as SoupBase
# The twitter XML file has nested 'url' tags
class BeautifulStoneSoup(SoupBase):
    pass
BeautifulStoneSoup.NESTABLE_TAGS['url'] = []

import bitly_api
BITLY_API = bitly_api.Connection('yuzeh', 'R_382aca6130ef4b2715f6cbd26999da64')

def grabCanonicalUrl(url):
    """Tries to resolve url using bit.ly api."""
    try:
        result = BITLY_API.expand(shortUrl=url)[0]
        if 'long_url' not in result: return url # Was not a bit.ly URL
        else: return result['long_url']
    except bitly_api.BitlyError as e:
#        print >> sys.stderr, str(e)
        return url

def grabDomain(url):
    """Grabs the domain name of the url, strips out 'www.'"""
    if not re.match('https?:\/\/', url):
        url = 'http://' + url
    ret = urlparse(url).netloc

    if re.match('^www\.', ret): return ret[4:]
    else: return ret

def grabTextTag(soup, tags):
    """Tries to follow the tree using xml tags. If not found return None."""
    s = soup
    for tag in tags:
        s = s.find(tag)
        if s == None: return None
    return s.find(text=True)

def extractFeatures(xmlStr):
    """Extracts features from tweets.  The features extracted are:
    - Hashtags (list of tags)
    - @Replies (list of names)
    - Retweet (name of retweeted user if retweeted, otherwise empty)
    - Author
    - length of tweet
    - number of punctuation marks
    - existence of hyperlink
    - domain of hyperlink
    """
    try:
        soup = BeautifulStoneSoup(xmlStr)
    except HTMLParseError:
        print >> sys.stderr, "Could not make soup from the xml string:"
        print >> sys.stderr, xmlStr
        return None

    if not soup.status:
        print >> sys.stderr, "This soup doesn't have a status tag:"
        print >> sys.stderr, xmlStr
        return None
    elif not soup.status.text:
        print >> sys.stderr, "This soup doesn't have any tweet text:"
        print >> sys.stderr, xmlStr
        return None

    # Mash all consecutive whitespace characters into a space
    text = re.sub('\s+', ' ', ''.join(soup.status.text.findAll(text=True)))
    author = grabTextTag(soup, ['status', 'user', 'id'])

    entities = soup.status.entities
    hashtags = [unicode(x.text.find(text=True))
       for x in entities.hashtags.findAll('hashtag')]
    replies = [unicode(x.id.find(text=True))
       for x in entities.user_mentions.findAll('user_mention')]
    print entities.urls.findAll('url', recursive=False)
    urls = [unicode(x.url.find(text=True))
       for x in entities.urls.findAll('url', recursive=False)]

    # remove hashtags, @replies, and urls from the tweet text
    entities = ['#' + hashtag for hashtag in hashtags] + \
               ['@' + reply for reply in replies] + \
               urls
    for entity in entities: 
        text = string.replace(text, entity, '')
    text = text.strip()

    tweetLength = len(text)
    numberOfPunctuation = sum([text.count(p) for p in '.:;?!\'",'])
    
    hyperlinkDomains = [grabDomain(grabCanonicalUrl(url)) for url in urls]
    return {'text' : text,
            'author' : author,
            'hashtags' : [x.lower() for x in hashtags],
            'replies' : replies,
            'domains' : [x.lower() for x in hyperlinkDomains],
            'length' : tweetLength,
            'punct' : numberOfPunctuation}

