from flask import request, jsonify
from . import web_blueprint
from ..ieee.issue import IssueController
from ..ieee.controller import Controller
from ..ieee.article import ArticleController
from ..ieee.journal import JournalController


@web_blueprint.route('/brief', methods=['GET'])
def handle_brief():
    issue_number = request.args.get('isnumber')
    issue = IssueController(issue_number)
    return jsonify(issue.get_article_brief())


@web_blueprint.route('/journals', methods=['GET'])
def handle_journals():
    journals = Controller.get_all_journals()
    resp = []
    for journal in journals:
        resp.append({
            'entry_number': journal.entry_number,
            'name': journal.name
        })
    return jsonify(resp)


@web_blueprint.route('/issues', methods=['GET'])
def handle_issues():
    journal_number = request.args.get('punumber')
    journal = JournalController(journal_number)
    issues = journal.get_all_issues()
    resp = []
    for issue in issues:
        resp.append({
            'entry_number': issue.entry_number,
            'year': issue.year,
            'number': issue.number,
            'status': issue.status
        })
    return jsonify(resp)


@web_blueprint.route('/unvisited', methods='GET')
def handle_unvisited():
    return jsonify(ArticleController.get_all_unvisited_brief())


@web_blueprint.route('/further', methods=['GET'])
def handle_further():
    return jsonify(ArticleController.get_all_need_further_brief())


@web_blueprint.route('/important', methods=['GET'])
def handle_further():
    return jsonify(ArticleController.get_all_important_brief())


@web_blueprint.route('/article', methods=['GET'])
def handle_article():
    article_number = request.args.get('arnumber')
    return jsonify(ArticleController(article_number).entry)
