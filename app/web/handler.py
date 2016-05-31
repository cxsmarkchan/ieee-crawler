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
    return jsonify({
        'data': issue.get_article_brief()
    })


@web_blueprint.route('/journals', methods=['GET'])
def handle_journals():
    journals = Controller.get_all_journals()
    resp = []
    for journal in journals:
        resp.append({
            'entry_number': journal.entry_number,
            'name': journal.name
        })
    return jsonify({'data': resp})


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
    return jsonify({'data': resp})


@web_blueprint.route('/unvisited', methods=['GET'])
def handle_unvisited():
    return jsonify({
        'data': ArticleController.get_all_unvisited_brief()
    })


@web_blueprint.route('/further', methods=['GET'])
def handle_further():
    return jsonify({
        'data': ArticleController.get_all_need_further_brief()
    })


@web_blueprint.route('/important', methods=['GET'])
def handle_important():
    return jsonify({
        'data': ArticleController.get_all_important_brief()
    })


@web_blueprint.route('/all', methods=['GET'])
def handle_all():
    status = int(request.args.get('status'))
    return jsonify({
        'data': ArticleController.get_brief_by_status(status)
    })


@web_blueprint.route('/article', methods=['GET'])
def handle_article():
    article_number = request.args.get('arnumber')
    return jsonify({
        'data': ArticleController(article_number).entry
    })


@web_blueprint.route('/note', methods=['POST'])
def handle_note():
    article_number = request.form['arnumber']
    note = request.form['note']
    article = ArticleController(article_number)
    article.note = note
    return jsonify({'message': 'Success'})


@web_blueprint.route('/status', methods=['POST'])
def handle_status():
    article_number = request.form['arnumber']
    status = int(request.form['status'])
    article = ArticleController(article_number)
    article.status = status
    return jsonify({'message': 'Success'})
