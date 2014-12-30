#!/usr/bin/env python

"""
Add the GitHub "parent" repository to the current local repostory as the
"upstream" remote.

The "parent" GitHub repository is the repository from which the GitHub repo has
been forked from.

E.g. if your local repository contains this:

        # Output from `git remote -v`
        origin  git@github.com:sitaktif/foo (fetch)
        origin  git@github.com:sitaktif/foo (push)

...then this script will make it look like this:

        # Output from `git remote -v`
        origin  git@github.com:sitaktif/foo (fetch)
        origin  git@github.com:sitaktif/foo (push)
        upstream    https://github.com/SirVer/foo (fetch)
        upstream    https://github.com/SirVer/foo (push)

Amend the `USER` and `GITHUB_TOKEN` constants accordingly before use.
"""

from __future__ import print_function

import re
import subprocess
import requests

# Mandatory parameters
USER = 'your_user'             # Change this to your user
GITHUB_TOKEN = 'your_api_key'  # Generate a key on GitHub

# Other parameters
ORIGIN_REMOTE = 'origin'
UPSTREAM_REMOTE = 'upstream'

# To check whether the user seems to own the 'origin' repo
# Warning: it cannot really check whether it is a real Github repo or not
# (because it could be an arbitrary GitHub Enterprise url) and will fail later
# if it's not.
RE_USER_OWNS_ORIGIN = re.compile(r'^(?P<remote>%s)\s+'                # ORIGIN_REMOTE
                                 r'(?P<github_proto>\S+)(?:://|@)'    # https:// or git@
                                 r'(?P<github_url>\S+)[:/]'
                                 r'(?P<user>%s)/'                     # USER
                                 r'(?P<repo>[^/]+).git\s+'
                                 r'\(fetch\)\s*(?:$|\n)'
                                 r'' % (ORIGIN_REMOTE, USER))

# Does the repo have 'upstream' in its remotes
RE_REMOTE_HAS_UPSTREAM = re.compile(r'(^|\n)%s\s+' % UPSTREAM_REMOTE)

# Get information about the 'origin' repository
RE_ORIGIN_REMOTE_INFO = re.compile(r'^(?P<remote>%s)\s+'              # ORIGIN_REMOTE
                                   r'(?P<github_proto>\S+)(?:://|@)'  # https:// or git@
                                   r'(?P<github_url>\S+)[:/]'
                                   r'(?P<user>%s)/'                   # USER
                                   r'(?P<repo>[^/]+).git\s+'
                                   r'\(fetch\)\s*(?:$|\n)'
                                   r'' % (ORIGIN_REMOTE, USER))


class GitHub(object):
    """
    GitHub object to abstract calls to the GH API (public and enterprise).
    """

    ACCEPT_HEADER = {'Accept': 'application/vnd.github.v3+json'}

    @classmethod
    def _api_url(cls, github_url):
        if github_url == 'github.com':
            return 'https://api.github.com'
        else:
            return 'https://%s/api/v3' % github_url

    def _additional_headers(self):
        headers = self.ACCEPT_HEADER
        headers.update({'Authorization': 'token %s' % self.token})
        return headers

    def __init__(self, url, user, token):
        """
        Create a GH object (either GitHub or GitHub Enterprise)
        """
        self.url = url
        self.api_url = self._api_url(self.url)
        self.user = user
        self.token = token

    def _get_foo(self, foo):
        url = '%s/%s' % (self.api_url, foo)
        print("Request: %s" % url)
        return requests.get(url, headers=self._additional_headers())

    def get_repo(self, repo, user=None):
        if user is None:
            user = self.user
        return self._get_foo('repos/%s/%s' % (user, repo))


def main():

    remote_out = subprocess.check_output('git remote -v', shell=True,
                                         universal_newlines=True)
    if RE_USER_OWNS_ORIGIN.match(remote_out) is None:
        print("Current repository's '%s' remote does not seem to be owned "
              "by user '%s'. Skipping." % (UPSTREAM_REMOTE, USER))
        exit(0)

    if RE_REMOTE_HAS_UPSTREAM.search(remote_out):
        print("Repo already has a '%s' remote. Skipping." % UPSTREAM_REMOTE)
        exit(0)

    match = RE_ORIGIN_REMOTE_INFO.search(remote_out)
    if match is None:
        print("Could not parse the output of the repo's remote command:")
        print(remote_out)
        exit(1)

    # Get info about the current repo
    grps = match.groupdict()
    github_url, user, repo = grps['github_url'], grps['user'], grps['repo']
    ghub = GitHub(github_url, user, GITHUB_TOKEN)

    # Extract the parent url and add the remote
    repo_res = ghub.get_repo(repo)
    repo_json = repo_res.json()
    parent_repo_url = repo_json['parent']['html_url']
    subprocess.check_call('git remote add %s %s' % (
        UPSTREAM_REMOTE, parent_repo_url),
        shell=True)

if __name__ == '__main__':
    main()
