import twitter.management.commands.extract as extract
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

import abc

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
