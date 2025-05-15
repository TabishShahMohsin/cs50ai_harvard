import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    transition_dict = dict()

    if not corpus[page]:
        for page_in_corpus in corpus:
            transition_dict[page_in_corpus] = (1/len(corpus))
        return transition_dict

    for linked_page in corpus[page]:
        transition_dict[linked_page] = damping_factor / len(corpus[page]) + (1 - damping_factor) / len(corpus)

    for other_page in corpus:
        if other_page not in transition_dict:
            transition_dict[other_page] = (1 - damping_factor) / len(corpus)

    return transition_dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = dict()
    for i in corpus:
        page_rank[i] = 0

    page = random.choice(list(corpus.keys()))
    page_rank[page] = 1
    for i in range(n-1):
        trans_model = transition_model(corpus, page, damping_factor)
        page = random.choices(list(trans_model.keys()), weights=list(trans_model.values()), k=1)[0]
        page_rank[page] += 1

    total = sum(page_rank.values())

    for i in page_rank:
        page_rank[i] /= total

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    def over_margin(before_page_rank, after_page_rank, factor):
        error = 0
        for i in before_page_rank:
            error = max(error, abs(before_page_rank[i] - after_page_rank[i]))
        if error > factor:
            return True
        return False

    pagerank = dict()
    for i in corpus:
        pagerank[i] = 1/len(corpus)

    import copy
    _pagerank = copy.deepcopy(pagerank)
    while True:
        pagerank = copy.deepcopy(_pagerank)
        pr = (1 - damping_factor) / len(corpus)
        for i in corpus:
            _term = 0
            for j in corpus:
                if len(corpus[j]) == 0:
                    _term += pagerank[j] / len(corpus)
                elif i in corpus[j]:
                    _term += pagerank[j] / len(corpus[j])
            _pagerank[i] = pr + damping_factor * _term
        if not over_margin(pagerank, _pagerank, 0.001):
            break
            
    return pagerank


if __name__ == "__main__":
    main()
