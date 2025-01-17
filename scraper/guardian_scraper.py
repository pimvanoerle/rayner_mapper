import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List

import requests
from bs4 import BeautifulSoup
from dateutil import parser

from .article import Article

class GuardianScraper:
    BASE_URL = "https://www.theguardian.com"
    
    def __init__(self, output_dir: str = "../data/articles"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None
    
    def parse_article(self, url: str) -> Optional[Article]:
        soup = self.fetch_page(url)
        if not soup:
            return None
            
        try:
            # Extract article metadata
            title = soup.select_one("h1").get_text().strip()
            
            author_elem = soup.select_one("a[rel='author']")
            author = author_elem.get_text().strip() if author_elem else None
            
            date_elem = soup.select_one("details time")
            published_date = parser.parse(date_elem["datetime"]) if date_elem else datetime.now()
            
            # Extract content
            content_elements = soup.select("div[data-gu-name='body'] p")
            content = "\n".join([p.get_text().strip() for p in content_elements])
            
            # Extract restaurant name from title (part before the colon)
            restaurant_name = None
            if ":" in title:
                restaurant_name = title.split(":")[0].strip()
            
            # Extract section and tags
#            section = soup.select_one("nav[aria-label='Section'] a").get_text().strip()
#            tag_elements = soup.select("a[data-link-name='article tag']")
#            tags = [tag.get_text().strip() for tag in tag_elements]
            
            return Article(
                title=title,
                url=url,
                author=author,
                published_date=published_date,
                content=content,
                restaurant_name=restaurant_name,
#                section=section,
#                tags=tags
            )
            
        except Exception as e:
            print(f"Error parsing article {url}: {str(e)}")
            return None
    
    def save_article(self, article: Article):
        try:
            # Create filename from title
            safe_title = "".join(c if c.isalnum() else "_" for c in article.title)
            filename = f"{safe_title[:100]}.json"
            file_path = self.output_dir / filename
            
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(article.to_dict(), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving article {article.title}: {str(e)}")
            
    def scrape_section(self, section_url: str, limit: int = 10):
        """Scrape articles from a section page"""
        soup = self.fetch_page(section_url)
        if not soup:
            return
            
        article_links = soup.select("a[data-link-name='article']")
        processed = 0
        
        for link in article_links:
            if processed >= limit:
                break
                
            article_url = link.get("href")
            if not article_url.startswith("http"):
                article_url = self.BASE_URL + article_url
                
            article = self.parse_article(article_url)
            if article:
                self.save_article(article)
                processed += 1
                print(f"Saved article: {article.title}")
