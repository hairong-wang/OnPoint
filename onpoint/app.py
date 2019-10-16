# coding: utf8
# author: Hairong Wang

from flask import Flask, request, render_template
import logging
from logging import Formatter, FileHandler
import optparse
import json
import os
import re
import collections
import copy
import json
import time
import datetime

app = Flask(__name__)

def setup_app(app):
    '''set up some global configuration before defining other functions in the app'''
    logging.basicConfig(filename='app.log', level=logging.INFO)

setup_app(app)

@app.route("/")
def html_display():
    '''render html for root url'''
    return render_template("index.html")

@app.route("/query", methods=['POST'])
def get_result():
    '''
    Get answer for the question based on the context

    Returns:
        result (json str) -- a json string containing answer dictionary
    '''
    start_time = time.time()
    query = str(request.form['query_text'])
    query_text = query
    context_text = str(request.form['context_text'])
    result = process_query_wrapper(query_text, context_text)
    end_time = time.time()
    answer = json.loads(result)["answer"]
    log_file = open('query_records.log','a')
    log_file.write("Start Time: " + str(datetime.datetime.now()) + "; Query: " + query_text + "; Answer: " + answer + "; Time Used: " + str(end_time - start_time) + '\n')
    log_file.close()
    logging.info('time used = ', end_time - start_time)
    return result

def process_query(query_text: str, context_text: str):
    '''
    Get answer for the question based on the context

    Args:
        query_text (str) -- a question provided by user
        context_text (str) -- a paragraph from some article provided by user

    Returns:
        answer (str) -- the answer for the question extracted from the context
    '''
    if query_text is None:
        return None
    answer = 'No answer found'
    try:
      # convert context to squad test dataset format
      context = {"version": "v2.0",
                  "data": [{"title": "user_context",
                            "paragraphs": [{"qas": [{"question": query_text,
                                                    "id": "test"}],
                            "context": context_text}]}]}
      # write the converted test to a json file
      with open('tmp/data.json', 'w') as f:
        json.dump(context, f)
        f.close()
      # execute the model evaluation bash script which read the json file
      # and write predictions json file\
      os.system('bash data_pipeline/scripts/model_inference.sh tmp/data.json tmp')
      # read predictions json file to get answer
      prediction = {}
      with open('tmp/predictions.json') as f:
        prediction = json.load(f)
        f.close()
      answer = prediction['test']
    except Exception as e:
      logging.error(e)
    return answer

def process_query_wrapper(query_text: str, context_text: str):
    '''
    Wrapper for function 'process_query'

    Args:
        query_text (str) -- a question provided by user
        context_text (str) -- a paragraph from some article provided by user

    Returns:
        response (json str) -- a json string containing answer dictionary
    '''
    answer = process_query(query_text, context_text)
    response = json.dumps({"answer": answer})
    return response

if __name__ == '__main__':
    app.run(port=6001,debug=True)
