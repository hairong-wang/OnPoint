#!/usr/bin/env python
# coding: utf-8
# Author: Hairong Wang

import json
import pandas as pd
from nltk.translate.bleu_score import sentence_bleu

INFILE = "path/to/input/file"

class BleuScore:
    def __init__(self, infile):
        self._infile = infile

    def get_df(self):
        i = 0
        df = {}
        with open(self._infile, 'r') as fp:
            for line in fp:
                df[i] = json.loads(line)
                i += 1
        return pd.DataFrame.from_dict(df, orient='index')

    def calculate_BLEU_4_gram(self,record):
        reference = []
        for answer in record[0]['human_answers']:
            answer_array = answer.split(' ')
            reference.append(answer_array)
        candidate = record[0]['answers'][0]['text'].split(' ')
        score = sentence_bleu(reference, candidate,weights=(0, 0, 0, 1))
        return score

    #Add a column called BLEU_score to the qas column
    def add_BLEU_score(self, train_df):
        train_df_new = train_df.copy()
        bleu = []
        for i in range(train_df_new.shape[0]):
            record = train_df_new.loc[i]['qas']
            bleu.append(self.calculate_BLEU_4_gram(record))
        train_df_new['BLEU_4gram_score'] = bleu
        return train_df_new

def main():
    blue = BleuScore()
    train_df = blue.get_df(train_infile)
    train_df_small = train_df.head(100)
    train_df_new = blue.add_BLEU_score(train_df_small)
    train_df_new_sort = train_df_new.sort_values('BLEU_4gram_score',ascending=False)

if __name__=='__main__':
    main()
