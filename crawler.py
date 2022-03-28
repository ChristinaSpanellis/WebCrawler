import urllib.request, urllib.parse, validators
from bs4 import BeautifulSoup
from queue import Queue

crawl_limit = 100

def crawl(URL):
    urls_to_crawl = Queue(maxsize=100)
    urls_to_crawl.put(URL)
    urls_crawled = {URL}
    while (len(urls_crawled) != crawl_limit and not urls_to_crawl.empty()):
        next_url = urls_to_crawl.queue[0]
        try:
            response = urllib.request.urlopen(next_url)
            html_content = BeautifulSoup(response.read(), 'html.parser')
            for url in html_content.find_all('a'):
                if (not urls_to_crawl.full()):
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
        except Exception as e:
            urls_crawled.add(next_url)
            urls_to_crawl.get()
        if (len(urls_crawled) % 10 == 0):
            print(str(len(urls_crawled))+"/100 URLs crawled")
    return urls_crawled

def print_urls(urls_crawled):
    count = 1
    for url in urls_crawled:
        print(count + ": ", url)
        count += 1

def main():
    URL = str(input())
    if not validators.url(URL):
        print("Requested URL is malformed")
        exit()
    print("Requested URL:", URL)
    print_urls(crawl(URL))

if __name__ == "__main__":
    main()