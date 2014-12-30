github-utils
============

Various utilities for GitHub


github_add_upstream.py
----------------------

Add the *parent* repository (i.e. the repository I forked from initially on GitHub) to the
local repo, as the `upstream` remote. Do not overwrite the `upstream` remote if it already
exists.

To use this script, you will need:
    - python (2.x or 3.x)
    - python-requests (`pip install requests`)

You will need to update the `USER` and `GITHUB_TOKEN` constants.

Run with `./github_add_upstream.py`.
