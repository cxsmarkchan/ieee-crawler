from app.ieee.journal import JournalCrawler

if __name__ == '__main__':
    crawler = JournalCrawler(5165411)
    names, abstracts = crawler.get_current_issue_abstracts()
    with open('out/test.txt', mode='w', encoding='UTF-8') as fid:
        for number in names:
            fid.write('ID: ' + number + '\n')
            fid.write('NAME: ' + names[number] + '\n')
            fid.write('ABSTRACT: ' + abstracts[number] + '\n')
            fid.write('\n')
