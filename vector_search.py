import math
from collections import OrderedDict

import tf_idf
import lemmatization
from tf_idf import DocTfIdf
import inverted


def search(query: str):
    docs_to_word = inverted.get_dict_from_csv()
    docs_tf_idf = tf_idf.get_docs()

    query_lemms = [lemmatization.get_lem(word) for word in query.strip().split(' ')]
    query_dict = {}
    for word in set(query_lemms):
        docs_list = docs_to_word[word]
        tf = query_lemms.count(word) / len(docs_list) if len(docs_list) != 0 else 0
        idf = tf_idf.get_idf(docs_list)
        tf_idf_val = tf * idf
        query_dict.setdefault(word, tf_idf_val)
    print(query_dict)

    query_len = get_length(query_dict)

    results = dict()

    for doc in docs_tf_idf:
        doc_len = get_length(doc.words_dict)
        numerator = 0
        for word in query_dict.keys():
            numerator += doc.words_dict[word] * query_dict[word] if doc.words_dict.get(word) is not None else 0
        similarity = numerator / doc_len * query_len
        if similarity > 0:
            results.setdefault(similarity, doc.name)
    results = OrderedDict(results)
    print(results)
    results_list = [get_link(r.replace('.txt', '')) for r in results.values()]
    for i in results_list:
        print(i)


def get_length(dictionary: dict):
    len = math.sqrt(math.fsum(i ** 2 for i in dictionary.values()))
    return len


def get_link(num : str):
    links_dict = dict()
    with open('%s' % ("Links.txt"), 'r') as doc_file:
        for line in doc_file:
            link_list = line.strip().split(' - ')
            links_dict.setdefault(link_list[0], link_list[1])
    return links_dict[num]


if __name__ == "__main__":
    search("бездомная кошка")