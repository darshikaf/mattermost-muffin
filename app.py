#!flask/bin/python
from flask import Flask, jsonify, abort, request, Response
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
import json
import logging
import random
import re
import csv


logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

ix = open_dir("index")

app = Flask(__name__)

def search(text):
    return 'https://data.whicdn.com/images/287495565/original.gif'

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

@app.route('/muffin/api/v1/',methods=['POST'])
def index():
    resp_data = {
    "response_type": "in_channel", \
    "text": "Hello, world!"}
    resp = Response(content_type='application/json')
    resp.set_data(json.dumps(resp_data))
    return resp


'''
Initial try with hardcoded image url
'''
@app.route('/muffin/api/v1/new_post', methods=['POST'])
def new_post():
    resp_data = {"username": "giphy", "icon_url": "https://avatars0.githubusercontent.com/u/3588525?v=3&s=200", \
    "response_type": "in_channel", \
    "text": "`Darshika` searched for clap\n     https://raw.githubusercontent.com/darshikaf/gif-search-engine/master/gifs/clap.gif"}
    resp = Response(content_type='application/json')
    resp.set_data(json.dumps(resp_data))
    return resp

@app.route('/new_post', methods=['POST'])
def new_post_2():
    try:
        slash_command = False
        resp_data = {}
        #resp_data['username'] = 'USERNAME' #fix later
        #resp_data['icon_url'] = 'https://avatars0.githubusercontent.com/u/3588525?v=3&s=20' #fix later

        data = request.form
        #print(data)

        if 'token' not in data:
            raise Exception('Missing necessary token in the post data')
        
        #fix later
        '''
        if data['token'] not in MATTERMOST_GIPHY_TOKEN:
            raise Exception('Tokens did not match, it is possible that this request came from somewhere other than Mattermost')
        '''

        if 'command' in data:
            slash_command = True
            resp_data['response_type'] = 'in_channel'
        
        #alternative: outgoing webhook
        if not slash_command:
            translate_text = data['text'][len(data['trigger_word']):]
        

        #Exception is not handled 
        translate_text = data['text']
        #print(translate_text)
        if not translate_text:
            raise Exception("No translate text provided, not hitting Muffin")
        
        #Search query
        url = search_query(ix,translate_text)
        print(url)
        gif_url = url[0][0]
        #print(gif_url)
        
        if not gif_url:
            raise Exception('No gif url found for `{}`'.format(translate_text))
        
        resp_data['text'] = '''`{}` searched for {}
    {}'''.format(data.get('user_name', 'unknown').title(), translate_text, gif_url)

    except Exception:
         resp_data['text'] = 'Error occured'
    
    finally:
        resp = Response(content_type='application/json')
        resp.set_data(json.dumps(resp_data))
        logging.info(resp_data)
    #print(resp_data)
    
    #fix later
    '''
    except Exception as err:
        msg = err.message
        logging.error('unable to handle new post :: {}'.format(msg))
        resp_data['text'] = msg
    '''

    return resp

@app.route('/add_gif', methods=['POST'])
def add_gif():
    data = request.form
    #print(data)
    new_entry = data['text'].split(',')
    print('url={}'.format(new_entry[0]))
    print('tags={}'.format(new_entry[1]))
       
    with open("output.csv", "a") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows([new_entry])

    return  "{} was added to the repo.".format(new_entry[0])

if __name__ == '__main__':
    #make_index()
    app.run(host="0.0.0.0",debug=True)
