import os
import json

import prompt
import scraper
import preprocessing

from dotenv import load_dotenv
load_dotenv()


scraper = scraper.ArxivScraper(topic='music', num_papers=3)
papers = scraper.scrape()
for paper in papers:
    text = preprocessing.extract(paper['link'])
    print('.')
    chunks = preprocessing.chop(text)
    print('.')
    paper['summary'] = prompt.summarize(chunks)

    print(paper['summary'])

with open('papers.json', 'w') as fp:
    json.dump(papers, fp)
