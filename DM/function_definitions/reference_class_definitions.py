"""Define a class to represent Medline references:"""
class MLRef:
    def __init__(self, uid, authors, title, source, local_messages, abstract, url):
        self.uid = uid
        self.authors = authors
        self.title = title
        self.source = source
        self.local_messages = local_messages
        self.abstract = abstract
        self.url = url
        self.db = Medline

"""Define a class to represent EMBASE references:"""
class EMRef:
    def __init__(self, authors, title, publisher, publication_type):
        self.authors = authors
        self.title = title
        self.publisher = publisher
        self.publication.type = publication_type
        self.db = EMBASE

"""Define a class to represent CENTRAL references:"""
class CENRef:
    def __init__(self, authors, title, source, abstract, publication_type, url):
        self.authors = authors
        self.title = title
        self.source = source
        self.abstract = abstract
        self.publication_type = publication_type
        self.url = url
        self.db = CENTRAL




