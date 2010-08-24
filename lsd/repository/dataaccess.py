
"""Contains utilities for accessing data from the repository. This class is a
direct abstraction over the storage/database layer."""

class DAO(object):
    """The object that handles the data access process. Contains many utility
    methods for accessing the object from the database."""
    def __init__(self, 
