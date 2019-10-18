#!/usr/bin/env python
# coding: utf-8
# Author: Hairong Wang

import json
import pandas as pd

INFILE = "path/to/input/file"
OUTFILE = "path/to/output/file"

class SquadConverter:
    def __init__(self):
        self._template = SquadTemplate()

    def get_df(self,
              infile):
        with open(infile) as f:
            data = json.load(f)
        amazonQA_100_df = pd.DataFrame.from_dict(data, orient='columns')
        return amazonQA_100_df

    def write_to_json_file(self,
                           outfile):
        with open(outfile, 'w') as file:
            json.dump(self._template._dataset, file)

    def create_train_paragraph(self,
                               context: str,
                               question: str,
                               qid: int,
                               answer: str,
                               is_impossible: bool):
        ''' Create training paragraph, allowing only one answer'''
        paragraph = {
            "qas": [
                {
                    "question": "placeholder",
                    "id": "placeholder",
                    "answers": [],
                    "is_impossible": False
                },
            ],
            "context": "placeholder"
        }
        paragraph["context"] = context
        paragraph["qas"][0]["question"] = question
        paragraph["qas"][0]["id"] = qid
        if not is_impossible:
            paragraph["qas"][0]["answers"].append(
                create_answer(context, answer))
        paragraph["qas"][0]["is_impossible"] = is_impossible
        return paragraph

    def create_eval_paragraph(self,
                              context: str,
                              question: str,
                              qid: int,
                              answer1: str,
                              answer2: str,
                              answer3: str,
                              answer4: str,
                              is_impossible: bool):
        ''' Create evaluation paragraph'''
        paragraph = {
            "qas": [
                {
                    "question": "placeholder",
                    "id": "placeholder",
                    "answers": [],
                    "is_impossible": False
                },
            ],
            "context": "placeholder"
        }
        paragraph["context"] = context
        paragraph["qas"][0]["question"] = question
        paragraph["qas"][0]["id"] = qid
        if not is_impossible:
            paragraph["qas"][0]["answers"].append(
                create_answer(context, answer1))
            paragraph["qas"][0]["answers"].append(
                create_answer(context, answer2))
            paragraph["qas"][0]["answers"].append(
                create_answer(context, answer3))
            paragraph["qas"][0]["answers"].append(
                create_answer(context, answer4))
        paragraph["qas"][0]["is_impossible"] = is_impossible
        return paragraph

    def create_answer(self,
                      context: str,
                      answer: str):
        answer_dict = {
            "text": answer,
            "answer_start": context.find(answer)
        }
        return answer_dict

    def add_paragraph(self,
                      paragraph):
        self._template._dataset["data"][0]["paragraphs"].append(paragraph)

    # get context, question from amazonqa_squad dataframe, get index as qid
    def get_context_and_question_and_id(self, df, index):
        context = amazonQA_100_df.iloc[index]['context']
        question = amazonQA_100_df.iloc[index]['qas'][0]['question']
        qid = index
        return context, question, qid

class SquadTemplate:
    def __init__(self):
        self._dataset = {
            "version": "v2.0",
            "data": [
                {
                    "title": "amazon reviews",
                    "paragraphs": []
                },
            ]
        }

def main():
    '''example of converting amazonqa to squad format'''
    converter = SquadConverter()
    # read amazonqa dataset from json file into DataFrame
    df = converter.get_df(INFILE)
    # get context, question and id for the first record
    context, question, qid = converter.get_context_and_question_and_id(df,
                                                                       0)
    # assume this question has no answer
    is_impossible = True
    answer = converter.create_answer(context,
                                     "")
    # create training paragraphs
    paragraph = converter.create_train_paragraph(context,
                                                 question,
                                                 qid,
                                                 answer,
                                                 is_impossible)
    converter.add_paragraph(paragraph)
    converter.write_to_json_file(OUTFILE)
