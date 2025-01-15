import requests 
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque

class RecursiveWebCrawler:
    def clean_links(self, allLinks, start_url):
        cleanedLinks = []
        base_domain = urlparse(start_url).netloc
        for link in allLinks:
            if 'href' not in link.attrs:
                continue

            url = urljoin(start_url, link['href'])
            if url.startswith("http") and urlparse(url).netloc == base_domain:
                cleanedLinks.append(url)
                print(url)
        return cleanedLinks

    def crawl_page(self, url, visited=None):
        if visited is None:
            visited = set()
        
        if url in visited:
            return
        
        visited.add(url)
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            allLinks = soup.find_all("a")
            cleanedLinks = self.clean_links(allLinks, url)
            for link in cleanedLinks:
                if link not in visited:
                    self.crawl_page(link, visited)

        except Exception as e:
            print(e)

        return visited

class BFSWebCrawler:
    def __init__(self, start_url):
        self.start_url = start_url
        self.visited = set()
        self.base_domain = urlparse(start_url).netloc

    def clean_links(self, soup, current_url):
        cleaned_links = set()
        for link in soup.find_all('a'):
            if 'href' not in link.attrs:
                continue

            url = urljoin(current_url, link['href'])
            parsed = urlparse(url)
            if parsed.scheme.startswith('http') and parsed.netloc == self.base_domain:
                cleaned_links.add(url)
            
        return cleaned_links
    
    def crawl_page(self):
        queue = deque([self.start_url])
        while queue:
            current_url = queue.popleft()
            if current_url in self.visited:
                continue

            self.visited.add(current_url)
            try:
                response = requests.get(current_url)
                if response.status_code != 200:
                    continue
                
                soup = BeautifulSoup(response.content, 'html.parser')
                new_links = self.clean_links(soup, current_url)
                for link in new_links:
                    if link not in self.visited:
                        queue.append(link)
                        print(link)
                        
            except Exception as e:
                print(e)
                continue
        return self.visited
    
class DFSWebCrawler:
    def __init__(self, start_url):
        self.start_url = start_url
        self.visited = set()
        self.base_domain = urlparse(start_url).netloc

    def clean_links(self, soup, current_url):
        cleaned_links = set()
        for link in soup.find_all('a'):
            if 'href' not in link.attrs:
                continue

            url = urljoin(current_url, link['href'])
            parsed = urlparse(url)
            if parsed.scheme.startswith('http') and parsed.netloc == self.base_domain:
                cleaned_links.add(url)
            
        return cleaned_links
    
    def crawl_page(self):
        stack = [self.start_url]
        while stack:
            current_url = stack.pop()
            if current_url in self.visited:
                continue

            self.visited.add(current_url)
            try:
                response = requests.get(current_url)
                if response.status_code != 200:
                    continue
                
                soup = BeautifulSoup(response.content, 'html.parser')
                new_links = self.clean_links(soup, current_url)
                for link in new_links:
                    if link not in self.visited:
                        stack.append(link)
                        print(link)
                        
            except Exception as e:
                print(e)
                continue
        return self.visited

if __name__ == "__main__":
    start_url = sys.argv[1]
    crawler = BFSWebCrawler(start_url)
    all_links = crawler.crawl_page()


