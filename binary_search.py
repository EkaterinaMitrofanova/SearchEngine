import csv
import re
import pymorphy2
import inverted
import lemmatization

morph = pymorphy2.MorphAnalyzer()


def search(query: str) -> set:
    words_dict = inverted.get_dict_from_csv()

    docs = None
    for word in query.split():
        word = lemmatization.get_lem(word)
        docs_list = words_dict[word]
        if docs is None:
            docs = set(docs_list)
            continue
        docs.intersection_update(docs_list)
    return docs


if __name__ == "__main__":
    print(search('щенок поводырь'))
