import glob, json
import pandas as pd
from sys import argv
import spacy

def read_version(fname):
    with open(fname) as fin:
        j = json.load(fin)
    splt = fname.split('/')
    book = splt[-1].split('.')[0]
    version = splt[-2]
    return version, book, j


def do_book(b):
    proto = []
    version, book, content = read_version(b)
    for chapter, verses in content.items():
        for verse in verses:
            v = verse['verse']
            t = verse['text']
            proto.append({"version": version,
                          "book": book,
                          "chapter": chapter,
                          "verse": v,
                          "raw": t})
    return proto


def normalize(df):
    nlp = spacy.load("en_core_web_sm")
    def transform(raw):
        doc = nlp(raw)
        lemmas = [tok.lemma_.lower() for tok in doc if not (tok.is_punct or tok.is_stop)]
        norms = [tok.lower_ for tok in doc if not tok.is_punct]
        return lemmas, norms
    df["lemmatized"], df["normalized"] = zip(*df["raw"].map(transform))


def main(pattern="*/*.json"):
    books = glob.glob(pattern)
    proto = []
    print("read books")
    for b in books:
        proto.extend(do_book(b))
    df = pd.DataFrame(proto)

    print("normalize text")
    normalize(df)

    df.to_csv("bibles.csv", index=False)
    print("wrote bibles.csv")
    return df


if __name__ == "__main__":
    if len(argv) > 1:
        main(argv[1])
    else:
        main()