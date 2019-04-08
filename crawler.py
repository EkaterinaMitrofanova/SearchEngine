import re
import time

from grab import Grab
from weblib.error import DataNotFound

# base_url = 'https://pikabu.ru'
base_url = 'http://goodnewsanimal.ru'


def main():
    added = 0
    limit = 100
    count = 1
    stack = [base_url]
    doc_links = open("Links.txt", "w")

    for site in stack:
        stack_link = site
        print(str(added) + " - " + stack_link)

        g = Grab(log_file='html.html')
        g.go(stack_link)
        time.sleep(0.1)

        doc_file = open("docs/%i.txt" % added, "w")
        doc_file.write(g.doc.select("//*").text())
        doc_file.close()
        doc_links.write(str(added) + " - " + stack_link + '\n')

        added += 1
        if count == limit:
            continue
        for link in g.doc.select('//a'):
            try:
                href = base_url + link.attr("href")
            except DataNotFound:
                continue
            if count == limit:
                break
            if stack.count(href) == 0 and is_link_valid(href):
                stack.append(href)
                count += 1

    doc_links.close()


def is_link_valid(link):
    pattern_url = re.compile(base_url + '/news/.*')
    pattern_image = re.compile(".*.jpg$")
    # pattern_comment = re.compile(".*\\?cid=.*")
    pattern_comments = re.compile(".*#comments$")

    if link == base_url:
        return False
    if pattern_image.fullmatch(link):
        return False
    if not pattern_url.fullmatch(link):
        return False
    # if pattern_comment.fullmatch(link):
    #     return False
    if pattern_comments.fullmatch(link):
        return False
    return True


if __name__ == "__main__":
    main()