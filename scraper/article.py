from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, List

@dataclass
class Article:
    title: str
    url: str
    author: Optional[str]
    published_date: datetime
    content: str
    restaurant_name: Optional[str]
    section: Optional[str]
    tags: Optional[List[str]]
    
    def to_dict(self):
        article_dict = asdict(self)
        article_dict['published_date'] = self.published_date.isoformat()
        return article_dict