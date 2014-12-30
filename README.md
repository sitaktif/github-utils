github-utils
============

Various utilities for GitHub


github_add_upstream.py
----------------------

Add the *parent* repository (i.e. the repository I forked from initially on GitHub) to the
local repo, as the `upstream` remote. Do not overwrite the `upstream` remote if it already
exists.

If the local repository looks like this:

    # Output from `git remote -v`
    origin  git@github.com:sitaktif/foo (fetch)
    origin  git@github.com:sitaktif/foo (push)

...after running the script, it will eventually look like this (supposing I had initially forked the repository from the `someguy` user):

    # Output from `git remote -v`
    origin  git@github.com:sitaktif/foo (fetch)
    origin  git@github.com:sitaktif/foo (push)
    upstream    https://github.com/someguy/foo (fetch)
    upstream    https://github.com/someguy/foo (push)


### Running the script

To use this script, you will need:

* python (2.x or 3.x)
* python-requests (`pip install requests`)

You will also need to update the `USER` and `GITHUB_TOKEN` in the file, first.

Run with:

    `./github_add_upstream.py` # No arguments
