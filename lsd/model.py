import exceptions

"""Contains classes for types used in the frontend and backend and shit."""

class ModelException(exceptions.Exception):
    pass

class Type(object):
    STRING = 0
    INTEGER = 1
    FLOAT = 2
    LIST = 3
    REF = 4

class Tweet(object):
    properties = {
        'body'  : (Type.STRING,),
        'uid'   : (Type.INTEGER,),
        'time'  : (Type.TIMESTAMP,),}

    def __init__(self, **kargs):
        if set(kargs.keys()) != set(Tweet.properties.keys())
            raise ModelException, 
                "Tweet object not valid. Missing properties " 
                + set(Tweet.properties.keys()) - set(kargs.keys())
        self.__dict__.update(kargs)
