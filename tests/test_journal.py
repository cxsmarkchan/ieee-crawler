from unittest import TestCase
from app.ieee.journal import JournalCrawler


class TestJournalCrawler(TestCase):
    def setUp(self):
        # IEEE Transactions on Smart Grid
        self.__crawler = JournalCrawler(5165411)

    def test_get_article_numbers(self):
        url = 'http://ieeexplore.ieee.org/xpl/tocresult.jsp'
        issue_number = 7361791
        numbers = self.__crawler.get_article_numbers(
            url=url,
            issue_number=issue_number
        )
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

    def test_get_early_access_number(self):
        self.assertEqual(self.__crawler.get_early_access_number(),
                         '5446437')

    def test_get_articles(self):
        articles = self.__crawler.get_articles(['7399422'])
        self.assertEqual(
            articles['7399422'].title,
            'Sizing and Analysis of Renewable Energy and Battery Systems in Residential Microgrids'
        )

        self.assertEqual(
            articles['7399422'].abstract,
            'Accelerated development of eco-friendly technologies such as renewable energy, smart grids, and electric transportation will shape the future of electric power generation and supply. Accordingly, the power consumption characteristics of modern power systems are designed to be more flexible, which impact the system sizing. However, integrating these considerations into the design stage can be complex. Under these terms, this paper presents a novel model based on mixed integer linear programming for the optimization of a hybrid renewable energy system with a battery energy storage system in residential microgrids in which the demand response of available controllable appliances is coherently considered in the proposed optimization problem with reduced calculation burdens. The model takes into account the intrinsic stochastic behavior of renewable energy and the uncertainty involving electric load prediction, and thus proper stochastic models are considered. This paper investigates the effect of load flexibility on the component sizing of the system for a residential microgrid in Okinawa. Also under consideration are different operation scenarios emulating technical limitations and several uncertainty levels.'
        )
