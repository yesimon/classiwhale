import status.management.commands.extract as extract
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

import abc
import re

class ExtractorBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def ExtractWord(self, word):
        """Tokenizes a word. Returns None for unrecognized token"""
        return

    @abc.abstractmethod
    def ExtractStatus(self, status):
        """
        Extracts tokens from a tweet. Assumes status is a Status object the has
        properties for necessary metadata, so it can be many different types of
        objects.
        """
        return

    def _contains(string, query):
        return string.find(query) > -1


class SimpleExtractor(ExtractorBase):
    """
    Simple extractor is a simplistic extractor that tokenizes based on whitespace,
    strips certain punctuation symbols from words, removes stopwords, and 
    lowercases the result.
    """

    stopwords = stopwords.words('english')
    punctuation = ',.?;:"!\''

    @classmethod
    def ExtractWord(cls, word):
        word = word.strip(cls.punctuation).lower()
        if word in cls.stopwords:
            return None      
        return word

    @classmethod
    def ExtractStatus(cls, status):
        """
        Extract the tokens in a tweet based on ExtractWord. Unfortunately
        this is probably the bottleneck according to profiling
        """
        if not status.text: return None
        tokens = map(cls.ExtractWord, status.text.split())
        tokens = [w for w in tokens if w]
        return tokens
        
class BaltarExtractor(ExtractorBase):
    """
    Extractor which splits and tokenizes, strips punctation, removes stopwords,
    lowercases the results, and adds arbitrary metatokens.
    """

    stopwords = stopwords.words('english')
    splitre = re.compile('[^a-zA-Z0-9_$#@]+')

    # Expects word already lowercased
    @classmethod
    def ExtractWord(cls, word):
        pass

    @classmethod
    def ExtractStatus(cls, status):
        if not status.text or not status.user: return None
        allwords = status.text.lower().split()
        nolinkwords = []
        tokens = []
        for word in allwords:
            if word.startswith(('http://', 'https://', 'www.')):
                if word.find('bit.ly') > -1:
                    try:
                       w = extract.grabDomain(extract.grabCanonicalUrl(word)).lower()
                    except: 
                        # Exceeded bit.ly api rate limit 
                        w = extract.grabDomain(word).lower()
                else: w = extract.grabDomain(word).lower()
                tokens.append(w)
            else: nolinkwords.append(word)
        words = "".join(nolinkwords)
        words = cls.splitre.split(words)
        tokens.extend([w for w in words if (w not in cls.stopwords and w)])
        tokens.append('USER: {0}'.format(status.user.id))
        try: 
            reply_to_user_id = status.in_reply_to_user_id
            if reply_to_user_id: 
                tokens.append('IN_REPLY_TO_USER_ID: {0}'.format(reply_to_user_id))
        except: pass
        return tokens

class PorterBigramExtractor(ExtractorBase):
    """
    Extractor used for 229. Performs functionality of SimpleExtractor with also
    transforming urls into their canonical domains, extracting bigrams from
    the text, and adding an author token.
    """
    stopwords = stopwords.words('english')
    punctuation = ',.?;:"!\''
    stemmer = PorterStemmer()

    @classmethod
    def ExtractWord(cls, word):
        """
        Extract a word to get rid of punctuation, stems words, and changes 
        links to the domain only. Returns None for stopwords. Unfortunately
        this is probably the bottleneck according to profiling.
        """
        word = word.strip(cls.punctuation)
        if word.startswith(('http://', 'https://', 'www.')) or \
                cls._contains(word, '.com') or cls._contains(word, '.ly'):
            if cls._contains(word, 'bit.ly'):
                #return extract.grabDomain(word).lower()
                # Exceeded bit.ly api rate limit
                try:
                    return extract.grabDomain(extract.grabCanonicalUrl(word)).lower()
                except: pass
            return extract.grabDomain(word).lower()
        word = word.lower()
        if word in cls.stopwords:
            return None      
        return cls.stemmer.stem(word)


    def ExtractStatus(cls, status):
        """
        Extract the tokens in a tweet based on ExtractWord. Also adds bigrams and 
        a metadata tag for author. Unfortunately this is probably the bottleneck 
        according to profiling
        """
        tokens = map(cls.ExtractWord, status.text.split())
        tokens = [w for w in tokens if w]
        bigram_finder = BigramCollocationFinder.from_words(tokens)    
        bigrams_tuple = bigram_finder.score_ngrams(BigramAssocMeasures.chi_sq)
        tokens.extend([bigram for bigram, score in bigrams_tuple])
        tokens.extend('AUTHOR: {0}'.format(status.author.id))
        return tokens
