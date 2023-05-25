from bs4 import BeautifulSoup
import requests


NUM_PAPERS = 30
topic = 'music'


class ArxivScraper(object):
    """
    Scrapper class for Arxiv scrapers.
    """
    def __init__(
        self, 
        topic: str,
        num_papers: int=50,
        initial_paper: int=0, 
    ):
        self.topic = topic
        self.num_papers = num_papers
        self.initial_paper = initial_paper
        self.url = f'https://arxiv.org/search/?query={self.topic}&searchtype=all&source=header&order=-announced_date_first&size=50&abstracts=show&start={self.initial_paper}'
        self.papers = list()
    
    def scrape(self):
        """
        Scrapes N papers from Arxiv.
        Returns dict with:
        * Title
        * Abstract
        * Link to full paper
        * Summary (empty: will be populated later)
        """
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")

        results = soup.find(id="main-container")
        paper_elements = results.find_all("li", class_="arxiv-result")
        paper_elements = paper_elements[self.initial_paper:self.num_papers]
        for paper in paper_elements:
            title = paper.find("p", class_="title is-5 mathjax").text
            abstract = paper.find("span", class_="abstract-full has-text-grey-dark mathjax").text
            link_to_full_paper = paper.select_one("a[href*=pdf]")["href"]

            parsed_paper = {
                'title': title,
                'abstract': abstract,
                'link': link_to_full_paper,
                'summary': '',
            }

            self.papers.append(parsed_paper)
            self.initial_paper += 1
            self.num_papers -= 1

        return self.papers
