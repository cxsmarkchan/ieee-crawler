import requests
import re
from pyquery import PyQuery
from mongoengine import DoesNotExist
from .. import logger
from ..models import Journal, Issue
from .issue import IssueController


class JournalController:
    def __init__(self, journal):
        if isinstance(journal, Journal):
            self.__journal = journal
        else:
            from .controller import Controller
            self.__journal = Controller.get_journal_object(str(journal))

    def __eq__(self, other):
        return isinstance(other, JournalController) \
                and self.__journal == other.__journal

    @property
    def entry_number(self):
        return self.__journal.entry_number

    @property
    def name(self):
        return self.__journal.name

    def get_current_issue(self):
        url = 'http://ieeexplore.ieee.org/xpl/mostRecentIssue.jsp'
        payload = {
            'punumber': self.__journal.entry_number
        }
        r = requests.get(url, params=payload)

        query = PyQuery(r.text)
        text = query('#jrnl-issue-hdr h2').text().strip()
        current_year = int(text[-4:])
        issue_number = int(text[6])

        try:
            current_issue = Issue.objects.get(
                journal_reference=self.__journal,
                status=Issue.CURRENT_ISSUE
            )
            if current_issue.year == current_year \
                    and current_issue.number == issue_number:
                logger.info('Current issue has not been updated')
                return IssueController(current_issue)
            else:
                logger.info('Current issue need to be updated')
                query_text = '#pi-%d li:eq(%d) a' % \
                             (current_issue.year, current_issue.number - 1)
                url = query(query_text).attr('href')
                current_issue.entry_number = re.search('(?<=isnumber=)[0-9]+', url).group(0)
                current_issue.status = Issue.PAST_ISSUE
                current_issue.save()
        except DoesNotExist:
            logger.info('Current issue does not exist in database')

        # does not exist or updated
        current_issue = Issue()
        current_issue.entry_number = 'current_' + self.__journal.entry_number
        current_issue.year = current_year
        current_issue.number = issue_number
        current_issue.journal_reference = self.__journal
        current_issue.status = Issue.CURRENT_ISSUE
        current_issue.save()
        logger.info('Current issue updated')
        return IssueController(current_issue)

    def get_early_access(self):
        try:
            issue = Issue.objects.get(
                journal_reference=self.__journal,
                status=Issue.EARLY_ACCESS
            )
            return IssueController(issue)
        except DoesNotExist:
            issue = Issue()

            url = 'http://ieeexplore.ieee.org/xpl/RecentIssue.jsp'
            payload = {
                'punumber': self.__journal.entry_number
            }
            r = requests.get(url, params=payload)
            query = PyQuery(r.text)
            url = query('#nav-article li:eq(2) a').attr('href')

            issue.entry_number = re.search('(?<=isnumber=)[0-9]+', url).group(0)
            issue.year = 0
            issue.number = 0
            issue.status = Issue.EARLY_ACCESS
            issue.is_current = False
            issue.journal_reference = self.__journal
            issue.save()

            return IssueController(issue)

    def get_past_issue(self, year, number):
        try:
            issue = Issue.objects.get(
                journal_reference=self.__journal,
                year=year,
                number=number
            )
            return IssueController(issue)
        except DoesNotExist:
            issue = Issue()
            issue.year = year
            issue.number = number
            issue.journal_reference = self.__journal
            issue.status = Issue.PAST_ISSUE

            url = 'http://ieeexplore.ieee.org/xpl/RecentIssue.jsp'
            payload = {
                'punumber': self.__journal.entry_number
            }
            r = requests.get(url, params=payload)
            query = PyQuery(r.text)

            query_text = '#pi-%d li:eq(%d) a' % \
                         (issue.year, issue.number - 1)
            url = query(query_text).attr('href')
            issue.entry_number = re.search('(?<=isnumber=)[0-9]+', url).group(0)

            issue.save()

            return IssueController(issue)






