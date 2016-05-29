from unittest import TestCase
from mongoengine.connection import connect, disconnect
from app.ieee.controller import Controller


disconnect('default')
connect('ieee_crawler_test')


class TestContoller(TestCase):
    def setUp(self):
        Controller.get_journal(5165411)
        Controller.get_journal(59)

    def test_get_all_journals(self):
        journals = Controller.get_all_journals()
        self.assertEqual(journals[0].entry_number, '5165411')
        self.assertEqual(journals[1].entry_number, '59')

    def test_get_journal(self):
        journal = Controller.get_journal(5165411)
        self.assertEqual(journal.entry_number, '5165411')
        self.assertEqual(journal.name, 'IEEE Transactions on Smart Grid')

    def test_get_journal_object(self):
        journal = Controller.get_journal_object(5165411)
        self.assertEqual(journal.entry_number, '5165411')
        self.assertEqual(journal.name, 'IEEE Transactions on Smart Grid')
