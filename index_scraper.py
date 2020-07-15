import requests
import re
from bs4 import BeautifulSoup
from datetime import date
from time import sleep

class IndexScraper():

    def __init__(self):
        self.today = date.today().strftime("%Y/%m/%d")
        self.starting_url = f"https://index.hu/gazdasag/{self.today}"
        self.day_number = int(self.starting_url[-2:])
        self.days_collected = 1
    
    def __str__(self):
        return f"This is a scraping tool for Index.hu created by me. The scraping will start with this url: {self.starting_url}"

    def _get_contents(self, links):
        
        for link in links:
            article_page = requests.get(link)
            print(article_page)
            article_soup = BeautifulSoup(article_page.text, "html.parser")
            article_page.close()
            try:
                article_name = article_soup.find("h1", class_ = "").text.strip()
            except AttributeError as e:
                print(f"{link}: The scraper probably went too fast, skipping this article")
                continue
            except Exception as e:
                raise e

            
            with open("title_output.txt", "a+", encoding="UTF-8") as w:
                w.write(article_name + "\n")
            w.close()

            try:
                texts = article_soup.find(class_="cikk-torzs").get_text().strip().replace("\n","").replace("Vannak, akiknek már nincsenek kérdéseik, És vannak, akik az Indexet olvassák.Támogass te is!","")
            except AttributeError as e:
                print(f"{link}: The scraper probably went too fast, skipping this article")
                continue
            except Exception as e:
                raise e

            with open("text_output.txt", "a+", encoding="UTF-8") as t:
                t.write(texts + " ")
            t.close()

            #article_page.close()
            print(article_name)
            article_name = ""

            sleep(2)

    def start_scrape(self):
        url = self.starting_url
        while self.days_collected < self.day_number:

            if self.days_collected % 3 == 0:
                print("In order the circumvent Response [509] we have to sleep for a while...")
                sleep(15)
            
            links = []
            page = requests.get(url)

            sleep(1.5)
            
            soup = BeautifulSoup(page.text, "html.parser")
            links = [a['href'] for a in soup.find_all(class_='cim', href=True)]
            page.close()

            self._get_contents(links)
            
            new_url = self.starting_url[:-2] + str(self.day_number-self.days_collected)
            print(f"Gathering a new day: {new_url}")
            url = new_url
            self.days_collected += 1

            sleep(3)

   

if __name__ == "__main__":
    #main()
    scraper = IndexScraper()
    print(scraper)
    scraper.start_scrape()

else:
    print("Index scraper tool is ready!")
