import json
import os, glob
import pandas as pd
import numpy as np
import re
from collections import Counter
from tqdm import tqdm
import matplotlib.pyplot as plt
import logging
logger = logging.getLogger(__name__)


class Language(object):
    """Simple Tokenizer for Lanugage

    """
    def __init__(self, name):
        """Construct Language

        :param name(str):       Name of the Language
        """
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {0: "SOS", 1: "EOS"}
        self.n_words = 2  # Count SOS and EOS
        self.max_length_token = 0

    @classmethod
    def SOS_TOKEN(cls):
        return 0

    @classmethod
    def EOS_TOKEN(cls):
        return 1

    def addSentence(self, sentence):
        for word in sentence.split(' '):
            self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            token_length = len(word)
            if token_length > self.max_length_token:
                self.max_length_token = token_length
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1

    def idxFromSentence(self, sentence):
        idx = [self.word2index[word] for word in sentence.split(' ')]
        idx.append(self.EOS_TOKEN())
        return idx

    def sentenceFromIdx(self, idx):
        logger.debug("Idx: {}".format(idx))
        sent = [self.index2word[i] for i in idx]
        return " ".join(sent[:-1])


def normalizeVerse(text):
    # Remove special character e.g. `<i> </i>`
    text = re.sub(r"\<(.*?)\>", "", text)

    # Add space before ending punctuation
    text = re.sub('([.,!?()])', r' \1 ', text)
    text = re.sub('\s{2,}', ' ', text)

    # Remove all case (using .lower())
    text = text.lower()

    return text


def createDataFrame(scrape_dir):
    bibleDirectories = next(os.walk(scrape_dir))[1]
    df = pd.DataFrame()
    for bible in tqdm(bibleDirectories):
        logger.info(f"Processing Bible: {bible}")
        book_dirs = glob.glob(os.path.join(scrape_dir, bible, "*.json"))
        for book_dir in tqdm(book_dirs):
            logger.debug(f"Processing Book: {book_dir}")
            with open(book_dir, "r") as f:
                book_data = json.loads(f.read())
            for chapter in book_data:
                tmp = pd.DataFrame(data=book_data[chapter])
                tmp['book'] = os.path.splitext(os.path.basename(book_dir))[0]
                tmp['chapter'] = int(chapter)
                tmp['version'] = bible
            df = df.append(tmp)
    print(df)
    return df


def getVerseText(df, bible, book, chapter, verse):
    return df[np.logical_and(np.logical_and(np.logical_and(df.book == bible, df.chapter == book), df.verse == chapter), verse)]

def main(scrape_dir):

    df = createDataFrame(scrape_dir)

    print(getVerseText(df, "niv", "gen",1,1))


    # df = createDataFrame(jsonFile)
    # print(df.head())

    # print(getVerseText(df, "Genesis", 1, 1))
    #
    # allWords = []
    # lang = Language("en-kjv")
    # for i in tqdm(df.index):
    #     row = df.iloc[i]
    #     allWords += row['normalized'].split(" ")
    #     lang.addSentence(row['normalized'])
    #
    # print("# Total Words: {}".format(len(allWords)))
    # print("# Unique Words: {}".format(lang.n_words))
    #
    # cnt = Counter(allWords)
    # freq = np.array(cnt.most_common())
    # print(freq[:,0])

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scrapedDataPath = os.path.abspath(os.path.expanduser("~/data/personal/bibleML/scrapedBibles"))
    # filePath = os.path.abspath(os.path.expanduser("~/data/personal/bibleML/KJV.json"))
    main(scrapedDataPath)