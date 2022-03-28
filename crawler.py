from urllib.error import HTTPError, URLError
import urllib.request, urllib.parse, validators, sys
from bs4 import BeautifulSoup
from queue import Queue

def crawl(URL, crawl_limit = 100):
    '''
    Crawls a given URL for further valid URLS, searching recursively through each subpage for more URLs.
    :param URL: (string) seed URL
    :param crawl_limit: (int) the number of unique URLs to be crawled, the default is 100
    :return: (set) crawled urls
    '''
    urls_to_crawl = Queue(maxsize=crawl_limit) 
    # set the queue size to crawl_limit to save time on pages 
    # with 100s of nested urls since only 100 unique urls need to be returned, this can be increased or ommitted to explore every possible url
    urls_to_crawl.put(URL)
    urls_crawled = {URL} # using a set to store URLs to avoid reporting duplicate URLs
    while (len(urls_crawled) != crawl_limit and not urls_to_crawl.empty()):
        next_url = urls_to_crawl.queue[0]
        try:
            response = urllib.request.urlopen(next_url)
            html_content = BeautifulSoup(response.read().decode('UTF-8', errors='ignore'), 'html.parser')
            if (not urls_to_crawl.full()):
                for url in html_content.find_all(href=True):
                    if (not urls_to_crawl.full()): # check again incase the queue fills up
                        potential_url = url.get('href')
                        if (potential_url != next_url):
                            parsed_url = urllib.parse.urlparse(potential_url)
                            if (parsed_url.netloc):
                                urls_to_crawl.put(potential_url)
                            elif (parsed_url.path):
                                urls_to_crawl.put(next_url + "/" + potential_url)
                            elif (parsed_url.query):
                                urls_to_crawl.put(next_url + "/" +potential_url)
            urls_crawled.add(next_url)
            urls_to_crawl.get()
        except HTTPError as e: # I decided to include URLs that return HTTP errors since the spec didn't specify whether only accessible URLs should be reported or not
            urls_crawled.add(next_url)
            urls_to_crawl.get()
        except URLError as e: # ignores URLs that are malformed or return non-http errors
            pass
            urls_to_crawl.get()
        if (len(urls_crawled) % 10 == 0):
            print(str(len(urls_crawled))+"/100 URLs crawled")
    return urls_crawled

def print_urls(urls_crawled):
    for count, url in enumerate(urls_crawled):
        print(str(count + 1) + ": " + url)

def main():
    if (not sys.argv[1]):
        print("Please specify a URL")
        exit()
    URL = sys.argv[1]
    if (URL[-1] == "/"): # removing the / to allow inputs without / at the end to be valid
        URL = URL[:-1] # eg. can accept http://google.com/ and http://google.com
    if not validators.url(URL):
        print("Requested URL is malformed")
        exit()
    print("Requested URL:", URL)
    print_urls(crawl(URL))

if __name__ == "__main__":
    main()