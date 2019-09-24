#coding: utf8
#author: Hairong Wang

from flask import Flask,request,render_template
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
  logging.basicConfig(filename='app.log',level=logging.INFO)

setup_app(app)

@app.route("/")
def html_display():
  return render_template("index.html")

@app.route("/query", methods=['POST'])
def get_query_and_context():
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
  print('time used = ', end_time - start_time)
  return result

def _process_query(query_text: str, context_text: str):
  if query_text is None:
    return None
  context = json.dumps({"version": "v2.0", "data": [{"title": "user_context", "paragraphs": [{"qas": [{"question": query_text, "id": "test"}], "context": context_text}]}]})
  answer = 'test_answer'
  return answer

def process_query_wrapper(query_text: str, context_text: str):
  answer = _process_query(query_text, context_text)
  response = json.dumps({"answer": answer})
  return response

if __name__ == '__main__':
  app.run(port=6001)
