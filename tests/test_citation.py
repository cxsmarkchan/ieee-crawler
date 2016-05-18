from unittest import TestCase
from app.ieee.citation import CitationLoader


class TestCitationLoader(TestCase):
    def setUp(self):
        self.__loader = CitationLoader([7399422, 7072554])

    def test_get_citations_html(self):
        text = self.__loader.get_citations_html()
        test_text = '\r\n'.join([
            '@ARTICLE{7399422,',
            '<br>',
            'author={R. Atia and N. Yamada},',
            '<br>  journal={IEEE Transactions on Smart Grid}, ',
            '<br> title={Sizing and Analysis of Renewable Energy and Battery Systems in Residential Microgrids}, ',
            '<br>  year={2016},',
            '<br>  volume={7},',
            '<br>  number={3},',
            '<br>  pages={1204-1213},',
            '<br>  abstract={Accelerated development of eco-friendly technologies such as renewable energy, smart grids, and electric transportation will shape the future of electric power generation and supply. Accordingly, the power consumption characteristics of modern power systems are designed to be more flexible, which impact the system sizing. However, integrating these considerations into the design stage can be complex. Under these terms, this paper presents a novel model based on mixed integer linear programming for the optimization of a hybrid renewable energy system with a battery energy storage system in residential microgrids in which the demand response of available controllable appliances is coherently considered in the proposed optimization problem with reduced calculation burdens. The model takes into account the intrinsic stochastic behavior of renewable energy and the uncertainty involving electric load prediction, and thus proper stochastic models are considered. This paper investigates the effect of load flexibility on the component sizing of the system for a residential microgrid in Okinawa. Also under consideration are different operation scenarios emulating technical limitations and several uncertainty levels.},',
            '<br>  keywords={battery storage plants;demand side management;distributed power generation;hybrid power systems;integer programming;linear programming;load forecasting;renewable energy sources;smart power grids;Okinawa;battery energy storage system;battery systems;demand response;eco-friendly technologies;electric load prediction;electric power generation;electric transportation;hybrid renewable energy system;load flexibility;mixed integer linear programming;power systems;residential microgrids;smart grids;Batteries;Home appliances;Load modeling;Microgrids;Optimization;Renewable energy sources;Stochastic processes;Design optimization;demand response;hybrid power systems;microgrids;performance analysis},',
            '<br>  doi={10.1109/TSG.2016.2519541},',
            '<br>  ISSN={1949-3053},',
            '<br>  month={May},}<br>@ARTICLE{7072554,',
            '<br>',
            'author={A. Spring and G. Wirth and G. Becker and R. Pardatscher and R. Witzmann},',
            '<br>  journal={IEEE Transactions on Smart Grid}, ',
            '<br> title={Grid Influences From Reactive Power Flow of Photovoltaic Inverters With a Power Factor Specification of One}, ',
            '<br>  year={2016},',
            '<br>  volume={7},',
            '<br>  number={3},',
            '<br>  pages={1222-1229},',
            '<br>  abstract={This paper discusses the influence of unintended reactive power flow caused by photovoltaic (PV) inverter systems with a power factor specification of one on the grid voltage and grid loss. In theory, the apparent power feed-in of these PV systems should be equal to the active power feed-in. Observations in distribution grids have shown a reactive power flow caused by these systems. The main purpose is, if this influence has to be considered in grid planning and power system management in smart grids. Therefore, measurement data of several low voltage grids is used. Three different scenarios for the unintended reactive power are simulated. Under normal operating conditions, the unintended reactive power is not relevant. Nevertheless, if voltage or overload problems are not explainable, they can be a result of the unintended reactive power flow. This approach is very helpful for network operators to locate and understand the reasons for grid problems.},',
            '<br>  keywords={Inverters;Load modeling;Low voltage;Power measurement;Reactive power;Solar power generation;Distributed power generation;inverters;photovoltaic (PV) systems;power system measurements;power system reliability;reactive power;smart grids;solar power generation;voltage control},',
            '<br>  doi={10.1109/TSG.2015.2413949},',
            '<br>  ISSN={1949-3053},',
            '<br>  month={May},}<br>',
            '\r\n'
        ])
        self.assertEqual(text, test_text)

    def test_get_bibtex(self):
        entries = self.__loader.get_bibtex()
        benchmark = [{
            'ENTRYTYPE': 'article',
            'ID': '7399422',
            'author': 'R. Atia and N. Yamada',
            'journal': 'IEEE Transactions on Smart Grid',
            'title': 'Sizing and Analysis of Renewable Energy and Battery Systems in Residential Microgrids',
            'year': '2016',
            'volume': '7',
            'number': '3',
            'pages': '1204-1213',
            'abstract': 'Accelerated development of eco-friendly technologies such as renewable energy, smart grids, and electric transportation will shape the future of electric power generation and supply. Accordingly, the power consumption characteristics of modern power systems are designed to be more flexible, which impact the system sizing. However, integrating these considerations into the design stage can be complex. Under these terms, this paper presents a novel model based on mixed integer linear programming for the optimization of a hybrid renewable energy system with a battery energy storage system in residential microgrids in which the demand response of available controllable appliances is coherently considered in the proposed optimization problem with reduced calculation burdens. The model takes into account the intrinsic stochastic behavior of renewable energy and the uncertainty involving electric load prediction, and thus proper stochastic models are considered. This paper investigates the effect of load flexibility on the component sizing of the system for a residential microgrid in Okinawa. Also under consideration are different operation scenarios emulating technical limitations and several uncertainty levels.',
            'keyword': 'battery storage plants;demand side management;distributed power generation;hybrid power systems;integer programming;linear programming;load forecasting;renewable energy sources;smart power grids;Okinawa;battery energy storage system;battery systems;demand response;eco-friendly technologies;electric load prediction;electric power generation;electric transportation;hybrid renewable energy system;load flexibility;mixed integer linear programming;power systems;residential microgrids;smart grids;Batteries;Home appliances;Load modeling;Microgrids;Optimization;Renewable energy sources;Stochastic processes;Design optimization;demand response;hybrid power systems;microgrids;performance analysis',
            'doi': '10.1109/TSG.2016.2519541',
            'issn': '1949-3053',
        }, {
            'ENTRYTYPE': 'article',
            'ID': '7072554',
            'author': 'A. Spring and G. Wirth and G. Becker and R. Pardatscher and R. Witzmann',
            'journal': 'IEEE Transactions on Smart Grid',
            'title': 'Grid Influences From Reactive Power Flow of Photovoltaic Inverters With a Power Factor Specification of One',
            'year': '2016',
            'volume': '7',
            'number': '3',
            'pages': '1222-1229',
            'abstract': 'This paper discusses the influence of unintended reactive power flow caused by photovoltaic (PV) inverter systems with a power factor specification of one on the grid voltage and grid loss. In theory, the apparent power feed-in of these PV systems should be equal to the active power feed-in. Observations in distribution grids have shown a reactive power flow caused by these systems. The main purpose is, if this influence has to be considered in grid planning and power system management in smart grids. Therefore, measurement data of several low voltage grids is used. Three different scenarios for the unintended reactive power are simulated. Under normal operating conditions, the unintended reactive power is not relevant. Nevertheless, if voltage or overload problems are not explainable, they can be a result of the unintended reactive power flow. This approach is very helpful for network operators to locate and understand the reasons for grid problems.',
            'keyword': 'Inverters;Load modeling;Low voltage;Power measurement;Reactive power;Solar power generation;Distributed power generation;inverters;photovoltaic (PV) systems;power system measurements;power system reliability;reactive power;smart grids;solar power generation;voltage control',
            'doi': '10.1109/TSG.2015.2413949',
            'issn': '1949-3053',
        }]

        self.assertEqual(entries, benchmark)
