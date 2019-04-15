import re
import time
from collections import OrderedDict
from grab import Grab
from weblib.error import DataNotFound


base_url = 'http://goodnewsanimal.ru'
coefficient = 0.85


class Doc(object):

    def __init__(self, rank: float, links: set):
        self.rank = rank
        self.links = links


rank_links_dict = dict()


def main(docs):
    g = Grab(log_file='html.html')
    for doc in docs:
        rank_links_dict.setdefault(doc, Doc(1/len(docs), set()))
        g.go(doc)
        time.sleep(0.1)
        for link in g.doc.select('//a'):
            try:
                href = link.attr("href")
                if not re.compile('http:.*').fullmatch(href):
                    if href == "/":
                        href = base_url
                    else:
                        href = base_url + link.attr("href")
            except DataNotFound:
                continue
            if is_link_valid(href):
                rank_links_dict[doc].links.add(href)
        print('%s : %i' % (doc, len(rank_links_dict[doc].links)))
    print()
    count(docs, 10)


def count(docs, iterations: int):
    for i in range(iterations):
        link_rank_dict = dict()
        for doc in docs:
            links = rank_links_dict[doc].links
            for link in links:
                if rank_links_dict.get(link) is not None:
                    rank_for_sum = rank_links_dict[doc].rank / len(links)
                    if link_rank_dict.get(link) is None:
                        link_rank_dict.setdefault(link, rank_for_sum)
                    else:
                        link_rank_dict[link] += rank_for_sum

        for (link, rank) in link_rank_dict.items():
            val = (1 - coefficient) / len(docs) + rank *  coefficient
            rank_links_dict[link].rank = val
            print('%s : %f' % (link, val))
        print()

    results_dict = dict()
    for (name, doc) in rank_links_dict.items():
        results_dict.setdefault(name, doc.rank)

    sorted_results = sorted(results_dict.items(), key=lambda kv: kv[1])
    sorted_results.reverse()

    doc_links = open("Page_rank.txt", "w")
    for (name, rank) in OrderedDict(sorted_results).items():
        doc_links.write('%s : %f\n' % (name, rank))
        print('%s : %f' % (name, rank))


def get_links(limit: int):
    links_dict = dict()
    with open('%s' % ("Links.txt"), 'r') as doc_file:
        for line in doc_file:
            if limit == 0:
                break
            link_list = line.strip().split(' - ')
            links_dict.setdefault(link_list[0], link_list[1])
            limit = limit - 1
    return links_dict.values()


def is_link_valid(link):
    pattern_image = re.compile(".*.jpg$")
    pattern_comments = re.compile(".*#comments$")

    if pattern_image.fullmatch(link):
        return False
    if pattern_comments.fullmatch(link):
        return False
    return True


if __name__ == "__main__":
    main(get_links(100))
