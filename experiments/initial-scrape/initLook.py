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
            book_name = os.path.splitext(os.path.basename(book_dir))[0]
            with open(book_dir, "r") as f:
                book_data = json.loads(f.read())
            for chapter in book_data:
                tmp = pd.DataFrame(data=book_data[chapter])
                tmp['verse'] = tmp['verse'].astype(int)
                tmp['book'] = book_name

                tmp['chapter'] = int(chapter)
                tmp['version'] = bible
                tmp['normalized'] = tmp.text.apply(lambda t: normalizeVerse(t))
                df = df.append(tmp)
    return df


def getVerseText(df, version, book, chapter, verse):
    tmp = df[df.version == version]
    logger.debug(f"Parseing by Version: \n{tmp}\n")

    tmp = tmp[tmp.book == book]
    logger.debug(f"Parseing by Book: \n{tmp}\n")
    print(tmp.chapter.unique())

    tmp = tmp[tmp.chapter == chapter]
    logger.debug(f"Parseing by Chapter: \n{tmp}\n")

    return df[np.logical_and(np.logical_and(np.logical_and(df.version == version, df.book == book), df.chapter == chapter), df.verse == verse)]



def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-rdf", "--rebuild-dataframe", default=False, action='store_true', help="Rebuild the dataframe")
    parser.add_argument("-rl", "--rebuild-languages", default=False, action='store_true', help="Rebuild the Languages")
    parser.add_argument("-d", "--scrape-dir",
                        default=os.path.abspath(os.path.expanduser("~/data/personal/bibleML/scrapedBibles")),
                        help="Directory Containing the Scraped Bible Data")
    parser.add_argument("-v", "--verbose", default=0, action='count', help="up log level")
    args = parser.parse_args()

    if args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(level=level)


    mainDFFile = os.path.join(args.scrape_dir, "full_dataframe.csv")



    if args.rebuild_dataframe:
        logger.info("Creating DataFrame from scratch")
        df = createDataFrame(args.scrape_dir)
        df.to_csv(mainDFFile)
    else:
        logger.info(f"Loading Dataframe from: {mainDFFile} ")
        df = pd.read_csv(mainDFFile)

    print(df.head())

    # print(df[np.logical_and(df.bible == "niv")])
    print(getVerseText(df, "niv", "gen",1,1))


    freq = {}
    for version in tqdm(df.version.unique()):
        logger.info(f"Processing Language in Version {version}")

        bv = df[df.version == version].reset_index()
        lngCountFile = os.path.join(args.scrape_dir, f"{version}_words.json")

        if args.rebuild_languages:
            logger.info("Creating Language from scratch")
            allWords = []
            for i in tqdm(bv.index):
                row = bv.iloc[i]
                allWords += row['normalized'].split(" ")

            logger.info("Creating Counter")
            cnt = Counter(allWords)

            with open(lngCountFile, "w") as f:
                f.write(json.dumps(cnt.most_common()))

            cnt = cnt.most_common()
        else:
            with open(lngCountFile, "r") as f:
                cnt = json.loads(f.read())

        freq[version] = np.array(cnt)

    print(freq['niv'][:10,0])



if __name__ == "__main__":
    main()