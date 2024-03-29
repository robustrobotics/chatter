""" A simple bot to manage code review/CI interactions with github """

import re
import logging
import json

import agithub

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass
logging.getLogger(__name__).addHandler(NullHandler())


class JenkinsBot(object):
    """ Abstract some of the http api interactions """
    def __init__(self, token, organization, repo_name):
        self.github = agithub.Github(token=token)
        self.repo_name = repo_name
        self.repo = self.github.repos[organization][self.repo_name]

    def set_status(self, sha, status):
        """ Set the status of the PR """
        logging.info("sha={}".format(sha))
        code, response = self.repo.statuses[sha].post(body=status)
        if code != 201:
            logging.warning("Couldn't post status (returned {})"
                    .format(code))
            logging.warning("Response: {}".format(json.dumps(response,
                indent=2)))
        else:
            logging.info("Set status successfully")

    def get_status(self, sha):
        """ Get the status of the PR """
        status, response = self.repo.commits[sha].status.get()
        if status != 200:
            logging.warning("Couldn't get status (returned {})"
                    .format(status))
            logging.warning("Response: {}".format(json.dumps(response,
                indent=2)))
            return None
        else:
            return response

    def post_comment(self, issue_number, comment):
        """ Post a comment to the specified issue """
        issue = self.repo.issues[issue_number]
        status, response = issue.comments.post(body={"body": comment})
        if status != 201:
            logging.warning("Couldn't post comment (returned %d)", status)
            logging.warning("Response: {}".format(json.dumps(response,
                indent=2)))
        else:
            logging.info("Posted comment successfully")

    def search_for_comment(self, issue_number, pattern):
        """ Search comments in the issue for regexp """
        issue = self.repo.issues[issue_number]
        status, response = issue.comments.get()
        if status != 200:
            logging.warning("Couldn't read comments (returned %d)", status)
            logging.warning("Response: {}".format(json.dumps(response,
                indent=2)))
            return None
        else:
            return (comment for comment in response if re.search(pattern, comment['body'], re.IGNORECASE))

    def get_pull_request(self, pr_number):
        status, response = self.repo.pulls[pr_number].get()
        if status != 200:
            logging.warning("Couldn't fetch pull request issue data (returned %d)", status)
            logging.warning("Response: {}".format(json.dumps(response,
                indent=2)))
            return None
        else:
            return response

    def pr_reviewed_by(self, pr_number):
        """ Determine if a PR has been reviewed """

        status, response = self.repo.pulls[pr_number].get()
        if status != 200:
            logging.warning("Couldn't fetch pull request data (returned %d)", status)
            logging.warning("Response: {}".format(json.dumps(response,
                indent=2)))
            raise RuntimeError()
        pr = response

        status, response = self.repo.issues[pr_number].comments.get(per_page=100)
        if status != 200:
            logging.warning("Couldn't fetch issue comments (returned %d)", status)
            logging.warning("Response: {}".format(json.dumps(response,
                indent=2)))
            raise RuntimeError()
        comments = response

        pr_author = pr['user']
        signoff_pattern = "lgtm|looks good to me"

        reviewed_by = None
        self_review = None

        for comment in comments:
            if re.search(signoff_pattern, comment['body'], re.IGNORECASE) and \
                comment['user']['id'] != pr['user']['id']:
                return comment, pr['head']['sha']
        return None, pr['head']['sha']
