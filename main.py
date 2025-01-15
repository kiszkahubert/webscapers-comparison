import requests 
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque

class RecursiveWebCrawler:
    def cleanLinks(allLinks, base_url):
        cleanedLinks = []
        base_domain = urlparse(base_url).netloc
        for link in allLinks:
            if 'href' not in link.attrs:
                continue

            val = urljoin(base_url, link['href'])
            if val.startswith("http") and urlparse(val).netloc == base_domain:
                cleanedLinks.append(val)
                print(val)
        return cleanedLinks

    def crawl_page(url, visited=None):
        if visited is None:
            visited = set()
        
        if url in visited:
            return
        
        visited.add(url)
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            allLinks = soup.find_all("a")
            cleanedLinks = cleanLinks(allLinks, url)
            for link in cleanedLinks:
                if link not in visited:
                    crawl_page(link, visited)

        except Exception as e:
            print(e)

        return visited

    start_url = sys.argv[1]
    all_visited = crawl_page(start_url)

class BFSWebCrawler:
    def __init__(self, start_url):
        self.start_url = start_url
        self.visited = set()
        self.base_domain = urlparse(start_url).netloc

    def clean_links(self, soup, current_url):
        cleaned_links = set()