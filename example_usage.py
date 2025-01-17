from scraper.guardian_scraper import GuardianScraper

def main():
    scraper = GuardianScraper()
    
    # Scrape some sections
    sections = [
        #"https://www.theguardian.com/technology",
        #"https://www.theguardian.com/science",
        "https://www.theguardian.com/food/series/jay-rayner-on-restaurants",
    ]
    
    for section_url in sections:
        print(f"\nScraping section: {section_url}")
        scraper.scrape_section(section_url, limit=5)

if __name__ == "__main__":
    main() 
