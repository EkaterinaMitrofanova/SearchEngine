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
        print(word)
        docs_list = words_dict[word]
        if docs is None:
            docs = set(docs_list)
            continue
        docs.intersection_update(docs_list)
    return docs


def get_link(num : str):
    links_dict = dict()
    with open('%s' % ("Links.txt"), 'r') as doc_file:
        for line in doc_file:
            link_list = line.strip().split(' - ')
            links_dict.setdefault(link_list[0], link_list[1])
    return links_dict[num]


if __name__ == "__main__":
    results = search('бегемот кошки')
    print(results)
    for i in results:
        print(get_link(i.replace('.txt', '')))