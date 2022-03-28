# WebCrawler
Basic web crawler to extract and return nested URLs in a requested web page.
Language: Python 3.8

# Usage

## Using Docker

First build the image 


```docker build --tag web-crawler .  ```

Start a container and run the image as follows, replacing {url} with your URL of choice.


```docker run web-crawler {url}```

## Without Docker

To run the code you'll first need to install two packages. [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) is a Python library for extracting data from HTML files. [Validators](https://validators.readthedocs.io/en/latest/) is a Python library for validating various data formats.


```pip3 install beautifulsoup4 validators```

Run the code as follows, replaing {url} with your URL of choice.


```python3 crawler.py {url}```