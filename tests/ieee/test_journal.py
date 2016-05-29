from unittest import TestCase
from mongoengine import connect
from mongoengine.connection import disconnect
from app.ieee.controller import Controller
from app.models import Issue

disconnect('ieee_crawler')
connect('ieee_crawler_test')


class TestJournalController(TestCase):
    def setUp(self):
        self.__crawler = Controller.get_journal(5165411)
        journal = Controller.get_journal_object(5165411)

        for issue in Issue.objects.filter(journal_reference=journal):
            issue.delete()

        issue = Issue()
        issue.journal_reference = journal
        issue.number = 2
        issue.year = 2016
        issue.status = Issue.CURRENT_ISSUE
        issue.save()

        issue = Issue()
        issue.entry_number = '7361791'
        issue.journal_reference = journal
        issue.number = 1
        issue.year = 2016
        issue.status = Issue.PAST_ISSUE
        issue.save()

    def tearDown(self):
        journal = Controller.get_journal_object(5165411)
        for issue in Issue.objects.filter(journal_reference=journal):
            issue.delete()

    def test_get_current_issue(self):
        current_issue = self.__crawler.get_current_issue()
        past_issue = self.__crawler.get_past_issue(2016, 2)

        self.assertEqual(past_issue.status, Issue.PAST_ISSUE)
        self.assertEqual(past_issue.entry_number, '7410169')
        self.assertEqual(past_issue.journal_name, 'IEEE Transactions on Smart Grid')
        self.assertEqual(past_issue.year, 2016)
        self.assertEqual(past_issue.number, 2)

        # TODO: use mock to construct response
        self.assertEqual(current_issue.journal_name, 'IEEE Transactions on Smart Grid')
        self.assertEqual(current_issue.status, Issue.CURRENT_ISSUE)
        self.assertEqual(current_issue.entry_number, 'current_5165411')
        self.assertEqual(current_issue.year, 2016)
        self.assertEqual(current_issue.number, 3)

    def test_get_past_issue(self):
        past_issue = self.__crawler.get_past_issue(2016, 1)
        self.assertEqual(past_issue.status, Issue.PAST_ISSUE)
        self.assertEqual(past_issue.entry_number, '7361791')
        self.assertEqual(past_issue.journal_name, 'IEEE Transactions on Smart Grid')
        self.assertEqual(past_issue.year, 2016)
        self.assertEqual(past_issue.number, 1)

    def test_get_early_access(self):
        early_access = self.__crawler.get_early_access()
        self.assertEqual(early_access.status, Issue.EARLY_ACCESS)
        self.assertEqual(early_access.entry_number, '5446437')
        self.assertEqual(early_access.journal_name, 'IEEE Transactions on Smart Grid')


