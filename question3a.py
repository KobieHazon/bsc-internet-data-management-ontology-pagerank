import requests
import lxml.html
from collections import deque
import sys

DEPTH_LIMIT = 3

def main(start_url):
    urls = crawler(start_url)
    if sys.argv[0] == "question3a.py":
        print_urls(urls)
    return urls


def crawler(start_url):
    urls = {}
    to_crawl = deque()
    cur_depth = 0
    to_crawl.append((cur_depth, start_url))
    while (len(to_crawl) != 0):
        cur_depth, current_url = to_crawl.popleft()
        if (current_url in urls):
            continue
        r = requests.get(current_url)
        page = lxml.html.fromstring(r.content)
        urls[current_url] = set()
        for link in page.xpath("//a[contains(@href, '/wiki/') and not(contains(@href, ':'))]/@href"):
            if (len(urls[current_url]) == 10):
                break
            full_link = wiki_dom + link
            if cur_depth < DEPTH_LIMIT:
                if full_link not in urls[current_url]:
                    urls[current_url].add(full_link)
                    to_crawl.append((cur_depth + 1, full_link))
            else:
                if (full_link in urls):
                    urls[current_url].add(full_link)

        if len(urls[current_url]) == 0:
            urls[current_url].add(current_url)
    return urls


def print_urls(urls):
    for key in urls.keys():
        string = str()
        string += key + "= {"
        for link in urls[key]:
            string += link + ", "
        string = string[0:len(string) - 2] + "}"
        print(string)


wiki_dom = "https://en.wikipedia.org"
if len(sys.argv) == 2:
    main(sys.argv[1])
