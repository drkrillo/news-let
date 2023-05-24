from bs4 import BeautifulSoup
import requests
import pdf_reader

SEARCH_TOPICS = [
    'python',
]
NUM_PAPERS = 30
topic = 'music'
paper_id = 0

URL = f'https://arxiv.org/search/?query={topic}&searchtype=all&source=header&order=-announced_date_first&size=50&abstracts=show&start={paper_id}'


page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="main-container")
paper_elements = results.find_all("li", class_="arxiv-result")

parsed_papers = []
for paper in paper_elements:
    title = paper.find("p", class_="title is-5 mathjax").text
    abstract = paper.find("span", class_="abstract-full has-text-grey-dark mathjax").text
    link_to_full_paper = paper.select_one("a[href*=pdf]")["href"]
    full_article = pdf_reader.extract_pdf_by_url(link_to_full_paper)

    print(full_article)
