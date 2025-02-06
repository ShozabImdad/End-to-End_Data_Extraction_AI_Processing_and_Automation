import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict
import logging

class BBCNewsScraper:
    def __init__(self):
        # Using BBC World News which has a simpler structure
        self.base_url = "https://www.bbc.com/news/world"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def fetch_articles(self) -> List[Dict]:
        try:
            logging.info(f"Fetching articles from {self.base_url}")
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = []
            
            # Find all article containers
            article_containers = soup.find_all('div', class_='sc-b8778340-3')
            
            if not article_containers:
                logging.warning("No article containers found. Trying alternative selectors...")
                # alternative selector
                article_containers = soup.find_all('div', {'data-entityid': lambda x: x and x.startswith('story')})
            
            logging.info(f"Found {len(article_containers)} potential articles")
            
            for container in article_containers:
                try:
                    # Find title
                    title_elem = container.find('h2', class_= 'sc-8ea7699c-3')
                    if not title_elem:
                        continue
                    title = title_elem.text.strip()
                    
                    # Find summary
                    summary_elem = container.find('p', class_= 'sc-b8778340-4')
                    if not summary_elem:
                        continue
                    summary = summary_elem.text.strip()
                    
                    if title and summary:
                        article = {
                            'title': title,
                            'summary': summary
                        }
                        articles.append(article)
                        logging.info(f"Found article: {title[:50]}...")
                
                except AttributeError as e:
                    logging.warning(f"Error parsing article container: {e}")
                    continue
            
            if not articles:
                logging.error("No articles could be parsed. HTML structure:")
                logging.error(soup.prettify()[:500])  # Log first 500 chars of HTML for debugging
            else:
                logging.info(f"Successfully scraped {len(articles)} articles")
            
            return articles
            
        except requests.RequestException as e:
            logging.error(f"Error fetching BBC News: {e}")
            return []
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            logging.error(f"Response status code: {response.status_code if 'response' in locals() else 'N/A'}")
            return []
            
    def save_to_csv(self, articles: List[Dict], filename: str = 'news_articles.csv'):
        if not articles:
            logging.warning("No articles to save")
            return
            
        df = pd.DataFrame(articles)
        df.to_csv(filename, index=False)
        logging.info(f"Saved {len(articles)} articles to {filename}")