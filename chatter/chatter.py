#!/usr/bin/env python
""" Front end to interact with github manually """

import os
import sys
import logging
import argparse

import jenkins_bot

def build(args):
    """ Set build status based on args """

    context = 'build'
    state = args.state
    sha = args.sha

    if sha is None:
        logging.error("""No commit hash available. Either pass a hash
                via --sha, or set the environment variable
                'ghprbActualCommit'.""")
        sys.exit(1)

    status = {'context': context, 'state': state}

    if args.description is not None:
        status['description'] = args.description
    elif state == 'success':
        status['description'] = "Build succeeded passed."
    elif state == 'failed':
        status['description'] = "Build failed."
    elif state == 'error':
        status['description'] = "There was an error building."
    elif state == 'pending':
        status['description'] = "Build results pending."

    if args.url is not None:
        status['target_url'] = args.url

    jenkins_bot.JenkinsBot(args.token).set_status(sha, status)

def tests(args):
    """ Set tests status based on args """
    context = 'tests'
    state = args.state
    sha = args.sha

    status = {'context': context, 'state': state}
    if sha is None:
        logging.error("""No commit hash available. Either pass a hash
                via --sha, or set the environment variable
                'ghprbActualCommit'.""")
        sys.exit(1)

    if args.description is not None:
        status['description'] = args.description
    elif state == 'success':
        status['description'] = "All tests passed."
    elif state == 'failed':
        status['description'] = "Some tests failed."
    elif state == 'error':
        status['description'] = "There was an error testing."
    elif state == 'pending':
        status['description'] = "Test results pending."

    if args.url is not None:
        status['target_url'] = args.url

    jenkins_bot.JenkinsBot(args.token).set_status(sha, status)

def code_review(args):
    """ Set code review status based on args """
    context = 'code_review'
    sha = args.sha
    issue = args.issue

    if issue is None:
        logging.error("""No commit hash available. Either pass an issue
                via --issue, or set the environment variable
                'ghprbPullId'.""")
        sys.exit(1)

    if sha is None:
        logging.error("""No commit hash available. Either pass a hash
                via --sha, or set the environment variable
                'ghprbActualCommit'.""")
        sys.exit(1)

    match = jenkins_bot.JenkinsBot(args.token).search_for_comment(issue,
            "lgtm|looks good to me")
    if match:
        state = 'success'
        description = 'Code review completed'
    else:
        state = 'pending'
        description = 'Code review pending'

    status = {'context': context, 'state': state, 'description': description}

    jenkins_bot.JenkinsBot(args.token).set_status(sha, status)

def main():
    """ Main function """
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("--sha", default=os.environ.get('ghprbActualCommit'),
            help="SHA hash of the commit for which to set status")
    parser.add_argument("--issue", help="Issue number to comment on",
        default=os.environ.get('ghprbActualCommit'))
    parser.add_argument("--url", help="URL to link to this update",
        default=os.environ.get('JOB_URL'))
    parser.add_argument("--token", help="Token to use for authentication",
        default=os.environ.get('GITHUB_AUTH_TOKEN'))
    parser.add_argument("--description", help="Description of status update")
    subparsers = parser.add_subparsers(help="commands")

    # Parser to set code review status
    code_review_parser = subparsers.add_parser("codereview",
            help="Check if code review has been completed")
    code_review_parser.set_defaults(command=code_review)

    # Parser to set build status
    build_parser = subparsers.add_parser("build",
            help="Set build check status")
    build_parser.set_defaults(command=build)

    # Parser to set test status
    tests_parser = subparsers.add_parser("tests",
            help="Set tests check status")
    tests_parser.set_defaults(command=tests)
    tests_parser.add_argument("state", help="State to set",
            choices=['success', 'pending', 'error', 'failure'])

    args = parser.parse_args()
    if args.token is None:
        logging.error("No authorization token supplied; please set"
                "environment variable GITHUB_AUTH_TOKEN")
        sys.exit(1)

    args.command(args)

if __name__ == '__main__':
    main()
