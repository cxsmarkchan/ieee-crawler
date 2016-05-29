from unittest import TestCase
from mongoengine.connection import connect, disconnect
from app.ieee.controller import Controller


disconnect('ieee_crawler')
connect('ieee_crawler_test')


class TestContoller(TestCase):
    def test_get_journal(self):
        journal = Controller.get_journal(5165411)
        self.assertEqual(journal.entry_number, '5165411')
        self.assertEqual(journal.name, 'IEEE Transactions on Smart Grid')

    def test_get_journal_object(self):
        journal = Controller.get_journal_object(5165411)
        self.assertEqual(journal.entry_number, '5165411')
        self.assertEqual(journal.name, 'IEEE Transactions on Smart Grid')
