import os
import csv
import re

file_path = 'inverted.csv'


def get_docs_to_word_dict() -> {}:
    directory = 'lemma/'
    files = os.listdir(directory)
    words_dict = {}
    for file in files:
        with open('%s%s' %(directory, file), 'r') as doc_file:
            for line in doc_file:
                for word in line.split():
                    word_docs = words_dict.setdefault(word, [])
                    if word_docs.count(file) == 0:
                        word_docs.append(file)
    return words_dict


def write_dict(dictionary):
    with open(file_path, "w", newline="") as file:
        w = csv.DictWriter(file, dictionary.keys())
        w.writeheader()
        w.writerow(dictionary)


if __name__ == "__main__":
    write_dict(get_docs_to_word_dict())


def get_dict_from_csv() -> {}:
    words_dict = {}
    with open(file_path) as fh:
        rd = csv.DictReader(fh, delimiter=',')
        for row in rd:
            words_dict.update(row)
    for (key, value) in words_dict.items():
        words_dict[key] = re.sub('[\[\]\']', '', value).split(', ')
    return words_dict
