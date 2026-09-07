import sys
import question3a


def print_prs(pr_dict):
    for key in pr_dict:
        print(key + ": " + str(pr_dict[key][0]))


def pr_calculator(in_urls, out_urls):
    pr_dict = {}
    df = 0.3
    random_url_pr = 1.0/len(in_urls)
    for key in in_urls:
        pr_dict[key] = [random_url_pr, random_url_pr]
    for i in range(1000):
        for key in pr_dict:
            val = 0
            for url in in_urls[key]:
                val += pr_dict[url][(i-1)%2]/len(out_urls[url])
            pr_dict[key][i%2] = df*random_url_pr + (1-df)*val
    return pr_dict


def in_url_generator(out_urls):
    in_urls = {key: set() for key in out_urls}
    for key in out_urls:
        for val in out_urls[key]:
            if val not in in_urls:
                in_urls[val] = set()
            in_urls[val].add(key)
    return in_urls


def main(url):
    out_urls = question3a.main(url)
    in_urls = in_url_generator(out_urls)
    prs = pr_calculator(in_urls, out_urls)
    print_prs(prs)


if len(sys.argv) == 2:
    given_url = sys.argv[1]
    main(given_url)
