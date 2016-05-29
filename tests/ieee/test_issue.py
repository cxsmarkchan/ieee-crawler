from unittest import TestCase
from mongoengine.connection import connect, disconnect
from app.ieee.controller import Controller
from app.models import Issue, Article


disconnect('ieee_crawler')
connect('ieee_crawler_test')


class TestIssueCrawler(TestCase):
    def setUp(self):
        # IEEE Transactions on Smart Grid
        self.__crawler = Controller.get_journal(5165411).get_past_issue(2016, 1)
        issue = Issue.objects.get(entry_number=self.__crawler.entry_number)
        for article in Article.objects.filter(issue_reference=issue):
            article.delete()
        for article in Article.objects.filter(entry_number='7399422'):
            article.delete()

    def test_crawl_article_numbers(self):
        numbers = self.__crawler.crawl_article_numbers()
        self.assertEqual(
            numbers,
            [
                '7361793', '7361800', '7270336', '7307227', '7271086',
                '7323868', '7128404', '7061965', '7095603', '7112181',
                '7095589', '7055343', '7152979', '7100914', '7064776',
                '7055363', '7063233', '7175042', '7122362', '7115170',
                '7063969', '7115166', '7121016', '7108042', '7273948',
                '7163618', '7052382', '7172536', '7152969', '7091026',
                '7127028', '7112542', '7127033', '7110380', '7173055',
                '7244250', '7064771', '7130652', '7161386', '7361794',
                '7361792', '7361698', '7017584', '6987318', '6998860',
                '6999960', '7063250', '7017597', '7056506', '6920036',
                '7045540', '7021935', '7083734', '7029711', '7047886',
                '7063236', '7322272', '7293228', '7361697', '7361795',
                '7361798', '7361801'
            ]
        )

    def test_crawl_articles(self):
        articles = self.__crawler.crawl_articles(['7399422'])
        self.assertEqual(
            articles['7399422'].title,
            'Sizing and Analysis of Renewable Energy and Battery Systems in Residential Microgrids'
        )
        self.assertEqual(
            articles['7399422'].author,
            'R. Atia and N. Yamada'
        )
        self.assertEqual(
            articles['7399422'].journal,
            'IEEE Transactions on Smart Grid'
        )
        self.assertEqual(
            articles['7399422'].year,
            '2016'
        )
        self.assertEqual(
            articles['7399422'].volume,
            '7'
        )
        self.assertEqual(
            articles['7399422'].number,
            '3'
        )
        self.assertEqual(
            articles['7399422'].pages,
            '1204-1213'
        )
        self.assertEqual(
            articles['7399422'].abstract,
            'Accelerated development of eco-friendly technologies such as renewable energy, smart grids, and electric transportation will shape the future of electric power generation and supply. Accordingly, the power consumption characteristics of modern power systems are designed to be more flexible, which impact the system sizing. However, integrating these considerations into the design stage can be complex. Under these terms, this paper presents a novel model based on mixed integer linear programming for the optimization of a hybrid renewable energy system with a battery energy storage system in residential microgrids in which the demand response of available controllable appliances is coherently considered in the proposed optimization problem with reduced calculation burdens. The model takes into account the intrinsic stochastic behavior of renewable energy and the uncertainty involving electric load prediction, and thus proper stochastic models are considered. This paper investigates the effect of load flexibility on the component sizing of the system for a residential microgrid in Okinawa. Also under consideration are different operation scenarios emulating technical limitations and several uncertainty levels.'
        )
        self.assertEqual(
            articles['7399422'].keyword,
            'battery storage plants;demand side management;distributed power generation;hybrid power systems;integer programming;linear programming;load forecasting;renewable energy sources;smart power grids;Okinawa;battery energy storage system;battery systems;demand response;eco-friendly technologies;electric load prediction;electric power generation;electric transportation;hybrid renewable energy system;load flexibility;mixed integer linear programming;power systems;residential microgrids;smart grids;Batteries;Home appliances;Load modeling;Microgrids;Optimization;Renewable energy sources;Stochastic processes;Design optimization;demand response;hybrid power systems;microgrids;performance analysis'
        )
        self.assertEqual(
            articles['7399422'].doi,
            '10.1109/TSG.2016.2519541'
        )
        self.assertEqual(
            articles['7399422'].issn,
            '1949-3053'
        )

        article_db = Article.objects.get(entry_number='7399422')
        self.assertEqual(article_db.entry_number, '7399422')
        self.assertEqual(article_db.title, articles['7399422'].title)
        self.assertEqual(article_db.author, articles['7399422'].author)
        self.assertEqual(article_db.journal, articles['7399422'].journal)
        self.assertEqual(article_db.year, articles['7399422'].year)
        self.assertEqual(article_db.volume, articles['7399422'].volume)
        self.assertEqual(article_db.number, articles['7399422'].number)
        self.assertEqual(article_db.pages, articles['7399422'].pages)
        self.assertEqual(article_db.abstract, articles['7399422'].abstract)
        self.assertEqual(article_db.keyword, articles['7399422'].keyword)
        self.assertEqual(article_db.doi, articles['7399422'].doi)
        self.assertEqual(article_db.issn, articles['7399422'].issn)
        self.assertEqual(article_db.status, Article.UNVISITED)