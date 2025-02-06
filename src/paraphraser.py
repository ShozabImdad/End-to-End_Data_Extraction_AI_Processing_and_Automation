import spacy
import random
from typing import List, Dict
import logging

class ContentParaphraser:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_lg')
        
    def get_synonyms(self, word: str) -> List[str]:
        # Simple synonym generation using word vectors
        ms = self.nlp.vocab.vectors.most_similar(
            self.nlp(word).vector.reshape(1, -1), n=5
        )
        return [self.nlp.vocab.strings[w] for w in ms[0][0] if w != 0]
        
    def paraphrase_text(self, text: str) -> str:
        doc = self.nlp(text)
        tokens = []
        
        for token in doc:
            if token.pos_ in ['NOUN', 'VERB', 'ADJ'] and not token.is_stop:
                synonyms = self.get_synonyms(token.text)
                if synonyms:
                    tokens.append(random.choice(synonyms))
                else:
                    tokens.append(token.text)
            else:
                tokens.append(token.text)
                
        return ' '.join(tokens)
        
    def process_articles(self, articles: List[Dict]) -> List[Dict]:
        processed_articles = []
        
        for article in articles:
            try:
                paraphrased_summary = self.paraphrase_text(article['summary'])
                processed_articles.append({
                    'original_title': article['title'],
                    'original_summary': article['summary'],
                    'paraphrased_summary': paraphrased_summary
                })
            except Exception as e:
                logging.error(f"Error processing article: {e}")
                continue
                
        return processed_articles