import requests
from bs4 import BeautifulSoup
import pandas as pd

class BookScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.current_page = 1
        self.data = []
    
    def fetch_page(self, page_number):
        url = f"{self.base_url}catalogue/page-{page_number}.html"
        response = requests.get(url)
        if response.status_code == 404:
            return None
        return BeautifulSoup(response.text, "html.parser")
    
    def extract_books(self, soup):
        books = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        for book in books:
            item = {
                "Title": book.find("img").attrs["alt"],
                "Link": book.find("a").attrs["href"],
                "Price": book.find("p", class_="price_color").text,
                "Stock": book.find("p", class_="instock availability").text.strip(),
            }
            self.data.append(item)
    
    def scrape_books(self):
        while True:
            print(f"Currently scraping page: {self.current_page}")
            soup = self.fetch_page(self.current_page)
            if not soup:
                break
            self.extract_books(soup)
            self.current_page += 1
    
    def save_to_csv(self, filename="books.csv"):
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

if __name__ == "__main__":
    scraper = BookScraper("https://books.toscrape.com/")
    scraper.scrape_books()
    scraper.save_to_csv()
