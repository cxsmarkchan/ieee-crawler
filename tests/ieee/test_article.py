from unittest import TestCase
from app.models import Article
from app.ieee.article import ArticleController


class TestArticleController(TestCase):
    def setUp(self):
        for article in Article.objects.filter(entry_number='7399422'):
            article.delete()

        article = Article()
        article.entry_number = '7399422'
        article.author = 'R. Atia and N. Yamada'
        article.journal = 'IEEE Transactions on Smart Grid'
        article.title = 'Sizing and Analysis of Renewable Energy and Battery Systems in Residential Microgrids'
        article.year = '2016'
        article.volume = '7'
        article.number = '3'
        article.pages = '1204-1213'
        article.abstract = 'Accelerated development of eco-friendly technologies such as renewable energy smart grids and electric transportation will shape the future of electric power generation and supply. Accordingly the power consumption characteristics of modern power systems are designed to be more flexible which impact the system sizing. However integrating these considerations into the design stage can be complex. Under these terms this paper presents a novel model based on mixed integer linear programming for the optimization of a hybrid renewable energy system with a battery energy storage system in residential microgrids in which the demand response of available controllable appliances is coherently considered in the proposed optimization problem with reduced calculation burdens. The model takes into account the intrinsic stochastic behavior of renewable energy and the uncertainty involving electric load prediction and thus proper stochastic models are considered. This paper investigates the effect of load flexibility on the component sizing of the system for a residential microgrid in Okinawa. Also under consideration are different operation scenarios emulating technical limitations and several uncertainty levels.'
        article.keyword = 'battery storage plants;demand side management;distributed power generation;hybrid power systems;integer programming;linear programming;load forecasting;renewable energy sources;smart power grids;Okinawa;battery energy storage system;battery systems;demand response;eco-friendly technologies;electric load prediction;electric power generation;electric transportation;hybrid renewable energy system;load flexibility;mixed integer linear programming;power systems;residential microgrids;smart grids;Batteries;Home appliances;Load modeling;Microgrids;Optimization;Renewable energy sources;Stochastic processes;Design optimization;demand response;hybrid power systems;microgrids;performance analysis'
        article.doi = '10.1109/TSG.2016.2519541'
        article.issn = '1949-3053'
        article.issue_reference = None
        article.status = Article.VISITED
        article.note = 'abc'
        article.save()

        self.__article = ArticleController('7399422')

    def test_bibtex(self):
        benchmark = '@article{7399422,\n' \
                    ' abstract = {Accelerated development of eco-friendly technologies such as renewable energy smart grids and electric transportation will shape the future of electric power generation and supply. Accordingly the power consumption characteristics of modern power systems are designed to be more flexible which impact the system sizing. However integrating these considerations into the design stage can be complex. Under these terms this paper presents a novel model based on mixed integer linear programming for the optimization of a hybrid renewable energy system with a battery energy storage system in residential microgrids in which the demand response of available controllable appliances is coherently considered in the proposed optimization problem with reduced calculation burdens. The model takes into account the intrinsic stochastic behavior of renewable energy and the uncertainty involving electric load prediction and thus proper stochastic models are considered. This paper investigates the effect of load flexibility on the component sizing of the system for a residential microgrid in Okinawa. Also under consideration are different operation scenarios emulating technical limitations and several uncertainty levels.},\n' \
                    ' author = {R. Atia and N. Yamada},\n' \
                    ' doi = {10.1109/TSG.2016.2519541},\n' \
                    ' issn = {1949-3053},\n' \
                    ' journal = {IEEE Transactions on Smart Grid},\n' \
                    ' keyword = {battery storage plants;demand side management;distributed power generation;hybrid power systems;integer programming;linear programming;load forecasting;renewable energy sources;smart power grids;Okinawa;battery energy storage system;battery systems;demand response;eco-friendly technologies;electric load prediction;electric power generation;electric transportation;hybrid renewable energy system;load flexibility;mixed integer linear programming;power systems;residential microgrids;smart grids;Batteries;Home appliances;Load modeling;Microgrids;Optimization;Renewable energy sources;Stochastic processes;Design optimization;demand response;hybrid power systems;microgrids;performance analysis},\n' \
                    ' number = {3},\n' \
                    ' pages = {1204-1213},\n' \
                    ' title = {Sizing and Analysis of Renewable Energy and Battery Systems in Residential Microgrids},\n' \
                    ' volume = {7},\n' \
                    ' year = {2016}\n' \
                    '}\n\n'

        self.assertEqual(self.__article.bibtex, benchmark)

    def test_entry(self):
        self.assertEqual(self.__article.entry, {
            'entry_number': '7399422',
            'title': 'Sizing and Analysis of Renewable Energy and Battery Systems in Residential Microgrids',
            'author': 'R. Atia and N. Yamada',
            'journal': 'IEEE Transactions on Smart Grid',
            'year': '2016',
            'volume': '7',
            'number': '3',
            'pages': '1204-1213',
            'abstract': 'Accelerated development of eco-friendly technologies such as renewable energy smart grids and electric transportation will shape the future of electric power generation and supply. Accordingly the power consumption characteristics of modern power systems are designed to be more flexible which impact the system sizing. However integrating these considerations into the design stage can be complex. Under these terms this paper presents a novel model based on mixed integer linear programming for the optimization of a hybrid renewable energy system with a battery energy storage system in residential microgrids in which the demand response of available controllable appliances is coherently considered in the proposed optimization problem with reduced calculation burdens. The model takes into account the intrinsic stochastic behavior of renewable energy and the uncertainty involving electric load prediction and thus proper stochastic models are considered. This paper investigates the effect of load flexibility on the component sizing of the system for a residential microgrid in Okinawa. Also under consideration are different operation scenarios emulating technical limitations and several uncertainty levels.',
            'keyword': 'battery storage plants;demand side management;distributed power generation;hybrid power systems;integer programming;linear programming;load forecasting;renewable energy sources;smart power grids;Okinawa;battery energy storage system;battery systems;demand response;eco-friendly technologies;electric load prediction;electric power generation;electric transportation;hybrid renewable energy system;load flexibility;mixed integer linear programming;power systems;residential microgrids;smart grids;Batteries;Home appliances;Load modeling;Microgrids;Optimization;Renewable energy sources;Stochastic processes;Design optimization;demand response;hybrid power systems;microgrids;performance analysis',
            'doi': '10.1109/TSG.2016.2519541',
            'issn': '1949-3053',
            'status': Article.VISITED,
            'note': 'abc'
        })

    def test_note(self):
        self.assertEqual(self.__article.note, 'abc')
        self.__article.note = 'abcd'
        self.assertEqual(self.__article.note, 'abcd')
        article = Article.objects.get(entry_number='7399422')
        self.assertEqual(article.note, 'abcd')

    def test_status(self):
        self.assertEqual(self.__article.status, Article.VISITED)
        self.__article.status = Article.IMPORTANT
        self.assertEqual(self.__article.status, Article.IMPORTANT)
        article = Article.objects.get(entry_number='7399422')
        self.assertEqual(article.status, article.IMPORTANT)
