from app.ieee.journal import JournalCrawler

if __name__ == '__main__':
    crawler = JournalCrawler(5165411)
    numbers = crawler.get_current_issue_numbers()
    print(numbers)
    print(len(numbers))
