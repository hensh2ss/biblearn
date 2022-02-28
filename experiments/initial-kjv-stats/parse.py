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


def createDataFrame(jsonFile):
    with open(jsonFile, "r") as f:
        data = json.loads(f.read())

    verses = []
    for book in data:
        for chapter in data[book]:
            for verse in data[book][chapter]:
                text = data[book][chapter][verse]
                verses.append({'book': book, 'chapter': chapter,
                               'verse': verse, 'text': text, 'normalized': normalizeVerse(text)})
    df = pd.DataFrame(data=verses)
    df.chapter = df.chapter.astype(int)
    df.verse = df.verse.astype(int)
    return df

def getVerseText(df, book, chapter, verse):
    return df[np.logical_and(np.logical_and(df.book == book, df.chapter == chapter), df.verse == verse)]

def main(jsonFile):
    df = createDataFrame(jsonFile)
    print(df.head())

    print(getVerseText(df, "Genesis", 1, 1))

    allWords = []

    for i in tqdm(df.index):
        row = df.iloc[i]
        allWords += row['normalized'].split(" ")

    print("# Total Words: {}".format(len(allWords)))
    print("# Unique Words: {}".format(len(set(allWords))))

    cnt = Counter(allWords)
    freq = np.array(cnt.most_common())

if __name__ == "__main__":
    filePath = os.path.abspath(os.path.expanduser("~/data/personal/bibleML/KJV.json"))
    main(filePath)