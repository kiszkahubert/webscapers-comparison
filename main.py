import requests 
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import re
from queue import PriorityQueue
import time 

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
                        
            except Exception as e:
                print(e)
                continue
        return self.visited
    
class FishSearchCrawler:
    def __init__(self, start_url, keywords):
        self.start_url = start_url
        self.visited = set()
        self.base_domain = urlparse(start_url).netloc
        self.keywords = keywords
        self.scores = {}
        
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
    
    def calculate_relevance(self, content, url):
        if not self.keywords:
            return len(content.find_all('a'))
            
        score = 0
        text = content.get_text().lower()
        for keyword in self.keywords:
            score += len(re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', text))
            
        url_lower = url.lower()
        for keyword in self.keywords:
            if keyword.lower() in url_lower:
                score += 2
                
        return score
    
    def crawl_page(self):
        pq = PriorityQueue()
        pq.put((0, 0, self.start_url))
        depth_map = {self.start_url: 0}
        while not pq.empty():
            relevance, depth, current_url = pq.get()
            if current_url in self.visited:
                continue

            self.visited.add(current_url)
            try:
                response = requests.get(current_url)
                if response.status_code != 200:
                    continue
                
                soup = BeautifulSoup(response.content, 'html.parser')
                relevance = self.calculate_relevance(soup, current_url)
                self.scores[current_url] = relevance
                if relevance > 0:
                    new_links = self.clean_links(soup, current_url)
                    for link in new_links:
                        if link not in self.visited:
                            new_depth = depth + 1
                            depth_map[link] = new_depth
                            pq.put((-relevance, new_depth, link))
                        
            except Exception as e:
                print(e)
                continue
                
        return self.visited, self.scores


if __name__ == "__main__":
    start_url = sys.argv[1]
    crawler1 = RecursiveWebCrawler()
    crawler2 = BFSWebCrawler(start_url)
    crawler3 = DFSWebCrawler(start_url)
    crawler4 = FishSearchCrawler(start_url, None)
    start_time = time.time()
    crawler1.crawl_page(start_url)
    end_time = time.time()
    print(f"Recursive crawler exec time: {end_time-start_time:.2f}s")
    start_time = time.time()
    crawler2.crawl_page()
    end_time = time.time()
    print(f"BFS crawler exec time: {end_time-start_time:.2f}s")
    start_time = time.time()
    crawler3.crawl_page()
    end_time = time.time()
    print(f"DFS crawler exec time: {end_time-start_time:.2f}s")
    start_time = time.time()
    crawler4.crawl_page()
    end_time = time.time()
    print(f"Fish Search crawler exec time: {end_time-start_time:.2f}s")