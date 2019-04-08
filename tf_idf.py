import math
import os
import re
import inverted
import pickle


class DocTfIdf(object):

    def __init__(self, name: str, words_dict: {str: float}):
        self.name = name
        self.words_dict = words_dict


def get_tf(word: str, doc: str):
    words = doc.strip().split(' ')
    return words.count(word)/len(words)


def get_idf(docs_list: []):
    return math.log10(100 / len(docs_list))


def get_tf_idf_list():
    words_dict = inverted.get_dict_from_csv()

    directory = 'lemma/'
    files = os.listdir(directory)

    docs_list = []

    for file in files:
        doc = DocTfIdf(file, {})
        with open('%s%s' %(directory, file), 'r') as doc_file:
            doc_file = doc_file.read()
            words = set(doc_file.strip().split(' '))
            for word in words:
                tf = get_tf(word, doc_file)
                word_docs_list = words_dict[word]
                idf = get_idf(word_docs_list)
                doc.words_dict.setdefault(word, tf * idf)
        docs_list.append(doc)
        print('%s - %i' % (file, len(words)))
    return docs_list


def save_docs(data: []):
    with open('tf_idf_docs.pickle', 'wb') as f:
        pickle.dump(data, f)
        print("-- Saved --")


def get_docs() -> [DocTfIdf]:
    with open('tf_idf_docs.pickle', 'rb') as f:
        data = pickle.load(f)
        return data


if __name__ == "__main__":
    docs = get_tf_idf_list()
    save_docs(docs)