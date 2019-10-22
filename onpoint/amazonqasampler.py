#!/usr/bin/env python
# coding: utf-8
# Author: Hairong Wang

import json
import pandas as pd

# Complete file name for amazonqa training dataset(squad format)
INFILE = "path/to/input/file"
OUTFILE = "path/to/output/file"

class AmazonQASampler:
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

    def sample(self):
        squad_train_df = self.get_df()
        amazonqa_sample = squad_train_df.sample(1000)
        return amazonQA_sample

def main():
    sampler = AmazonQASampler(INFILE)
    amazonqa_sample = sampler.sample()
    amazonqa_sample.to_json(OUTFILE)

if __name__=='__main__':
    main()
