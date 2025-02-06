from scraper import BBCNewsScraper
from paraphraser import ContentParaphraser
from gist_poster import GistPoster
import logging
import os
from dotenv import load_dotenv
import pandas as pd

def main():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Load environment variables
    load_dotenv()
    github_token = os.getenv('GITHUB_ACCESS_TOKEN')
    
    try:
        # Initialize components
        scraper = BBCNewsScraper()
        paraphraser = ContentParaphraser()
        gist_poster = GistPoster(github_token)
        
        # Scrape articles
        logging.info("Starting to scrape BBC News...")
        articles = scraper.fetch_articles()
        
        # Save original articles
        scraper.save_to_csv(articles, 'original_articles.csv')
        
        # Process and paraphrase articles
        logging.info("Paraphrasing articles...")
        processed_articles = paraphraser.process_articles(articles)
        
        # Save processed articles
        df = pd.DataFrame(processed_articles)
        df.to_csv('processed_articles.csv', index=False)
        
        # Post to Medium
        logging.info("Posting articles to Gist...")
        for article in processed_articles:
            gist_poster.create_post(article)
            
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()
