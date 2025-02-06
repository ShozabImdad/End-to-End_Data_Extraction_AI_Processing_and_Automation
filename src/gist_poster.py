import requests
import json
from typing import Dict
import logging

class GistPoster:
    def __init__(self, github_token: str):
        self.github_token = github_token
        self.api_url = "https://api.github.com/gists"
        self.headers = {
            'Authorization': f'Bearer {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def create_post(self, article: Dict, is_public: bool = False) -> str:
        try:
            gist_data = {
                "description": article['original_title'],
                "public": is_public,
                "files": {
                    f"{article['original_title']}.md": {
                        "content": f"# {article['original_title']}\n\n{article['paraphrased_summary']}"
                    }
                }
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=gist_data
            )
            response.raise_for_status()
            
            gist_url = response.json()['html_url']
            logging.info(f"Successfully created gist: {gist_url}")
            return gist_url
            
        except requests.RequestException as e:
            logging.error(f"Error creating gist: {e}")
            raise 