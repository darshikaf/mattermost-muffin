import re, pathlib, collections, array, struct, csv, math
from whoosh.fields import Schema, STORED, TEXT, ID, KEYWORD
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.query import Every
import os
import random

'''
Notes:
1. Creating schema and adding docs to the index are still separate
2. Adding docs to the csv file from slash commands still WIP
3. The urls are still pointing to giphy
4. Process to add gifs to artifactory needs to be decided
'''
def make_index():
    schema = Schema(url=ID(stored=True), tags=KEYWORD)
    if not os.path.exists("index"):
        os.mkdir("index")
        ix = create_in("index", schema)
        return ix

def add_docs(ix):
    writer = ix.writer()
    writer.add_document(url=u"https://media.giphy.com/media/26BkO5fkr0Kh7RhHG/giphy.gif", 
                        tags=u"sideeye react judge judging")
    writer.add_document(url=u"https://media.giphy.com/media/wbcMnfHqOJX9K/giphy.gif", 
                        tags=u"reaction react mindblown amazing wow")
    writer.add_document(url=u"https://media.giphy.com/media/wBNSbrYr7Eces/giphy.gif", 
                        tags=u"react celebrate welldone goodjob champange")
    writer.add_document(url=u"https://media.giphy.com/media/czwo5mMtaknhC/giphy.gif", 
                        tags=u"done finally free react")
    writer.add_document(url=u"https://media.giphy.com/media/qnOBmH70CGSVa/giphy.gif", 
                        tags=u"clap welldone goodjob applaud")
    writer.commit()


def search_query(ix,q):
    with ix.searcher() as searcher:
        query = QueryParser("tags", ix.schema).parse(q)
        results = searcher.search(query)
        file_path = [(r["url"],i) for i,r in enumerate(results)]
        #print(file_path)
        if len(file_path) > 1:
            file_path = [random.choice(file_path)]
        #return [(r["path"],i) for i,r in enumerate(results)]
        return(file_path)

if __name__ == '__main__':
    s = make_index()
    ix = open_dir("index")
    add_docs(ix)
    result = search_query(ix,'react')
    print(result)
    #print(ix.schema)
    #results = ix.searcher().search(Every('tags'))
    #for result in results:
    #    print (result['url'])
    
