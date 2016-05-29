from app.ieee.controller import Controller
import sys

if __name__ == '__main__':
    crawler = Controller.get_journal(sys.argv[1])
    mode = sys.argv[2]
    if mode == 'current':
        issue = crawler.get_current_issue()
    elif mode == 'early':
        issue = crawler.get_early_access()

    issue.update()
    articles = issue.get_article_brief()

    with open(sys.argv[3], 'w') as fid:
        for article in articles:
            fid.write(article['title'] + '\n')
