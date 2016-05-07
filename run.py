from app.ieee.journal import JournalCrawler
import sys

if __name__ == '__main__':
    crawler = JournalCrawler(sys.argv[1])
    mode = sys.argv[2]
    if mode == 'current':
        articles = crawler.get_current_issue(True)
    elif mode == 'early':
        articles = crawler.get_early_access(True)
    elif mode == 'new':
        articles = crawler.get_new_articles(True)
