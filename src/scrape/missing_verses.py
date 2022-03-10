import glob, json
from sys import argv

# run this script after format_xml2json.sh
# it reads all book jsons for a given version and flags missing content
# sometimes xpath has trouble pulling text from a chapter xml
# and that shows up as an empty chapter or empty verse in the book json

if __name__ == "__main__":
    version = argv[1]
    files = glob.glob("{}/*.json".format(version))
    total = 0
    for f in files:
        missing = 0
        try:
            with open(f) as fin:
                j = json.load(fin)
        except json.decoder.JSONDecodeError as jde:
            print(f, jde)
            total += 1
            continue

        for chapter, content in j.items():
            if not content:
                missing += 1
                continue
            for verse in content:
                if verse["text"] == "":
                    print(chapter, verse["verse"])
                    missing += 1
        print(f, missing)
        total += missing
    print(version, total)
