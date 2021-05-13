from bs4 import BeautifulSoup
import csv
import feedparser
import re
import requests

def search_article(url, phrases):
    response = requests.get(url)
    text = BeautifulSoup(response.text, 'html.parser').find('body').text
    for phrase in phrases:
        if re.search(r'\b' + re.escape(phrase) + r'\b', text):
            yield phrase

def search_rss(rss_entries, phrases):
    for entry in rss_entries:
        for hit_phrase in search_article(entry['link'], phrases):
            yield entry['link'], entry['title'], hit_phrase

def main(rss_url, phrases, output_csv_path, rss_limit=None):
    rss_entries = feedparser.parse(rss_url).entries[:rss_limit]
    with open(output_csv_path, 'w') as f:
        w = csv.writer(f)
        for url, title, phrase in search_rss(rss_entries, phrases):
            print('"{0}" found in "{1}"'.format(phrase, title))
            w.writerow([url, phrase])

if __name__ == '__main__':
    rss_url = 'https://www.cnbc.com/id/100727362/device/rss/rss.html'
    phrases = ['divorce', 'custody battle', …]
    main(rss_url, phrases, 'output.csv', 100)