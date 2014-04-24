#!/usr/bin/env python

"""test-git-browse.py, v0.2.0: Custom unit tests for git-browse Bash script"""

__author__ = "Nick Sawyer <nick@nicksawyer.net>"

import argparse
import os
import subprocess

# Set up options
parser = argparse.ArgumentParser()
parser.add_argument("-q", "--quiet", help="only show errors and summaries instead of all test output", action="store_true")
args = parser.parse_args()

# Set some variables in the environment for building Stash URLs
os.environ["TEST_STASH_URL_ROOT"] = "https://stash.mycompany.com"
os.environ["TEST_GITLAB_URL_ROOT"] = "https://gitlab.myorg.com"

DEFAULT_COMMAND_BASE = "git-browse --url-only "
DEFAULT_DIRECTORY = "foo/bar"
DEFAULT_FILENAME = "foo/bar/baz.ext"

# Define the different argument combinations to test
test_definitions = {
    "default": "",
    "branch": "--ref=test1",
    "tag": "--ref=1.0.0",
    "directory": "{0}",
    "directory-branch": "{0} --ref=test1",
    "directory-tag": "{0} --ref=1.0.0",
    "filename": "{0}",
    "filename-branch": "{0} --ref=test1",
    "filename-tag": "{0} --ref=1.0.0",
    "filename-line": "{0} --line=5",
    "filename-branch-line": "{0} --ref=test1 --line=5",
    "filename-tag-line": "{0} --ref=test1 --line=5",
    "commit": "092e8627fde84d5558c4429775d3498ec1ddce9a",
    "commits": "--commits",
    "commits-branch": "--commits --ref=test1",
    "commits-tag": "--commits --ref=1.0.0",
    "line": "--line=5",
    "branch-line": "--ref=test1 --line=5",
    "directory-line": "{0} --line=5",
    "commit-line": "092e8627fde84d5558c4429775d3498ec1ddce9a --line=5",
    "commits-line": "--commits --line=5",
    "raw": "--raw",
    "directory-raw": "{0} --raw",
    "filename-raw": "{0} --raw",
    "filename-branch-raw": "{0} --ref=test1 --raw",
    "filename-line-raw": "{0} --line=5 --raw",
    "filename-branch-line-raw": "{0} --ref=test1 --line=5 --raw",
    "commit-raw": "092e8627fde84d5558c4429775d3498ec1ddce9a --raw",
    "commits-raw": "--commits --raw",
    "blame": "--blame",
    "directory-blame": "{0} --blame",
    "filename-blame": "{0} --blame",
    "filename-branch-blame": "{0} --ref=test1 --blame",
    "filename-line-blame": "{0} --line=5 --blame",
    "filename-branch-line-blame": "{0} --ref=test1 --line=5 --blame",
    "commit-blame": "092e8627fde84d5558c4429775d3498ec1ddce9a --blame",
    "commits-blame": "--commits --blame",
    "raw-blame": "--raw --blame",
    "directory-raw-blame": "{0} --raw --blame",
    "filename-raw-blame": "{0} --raw --blame"
}

# These tests represent invalid use cases that should return an error for any host
error_tests = {
    "line": 64,
    "branch-line": 64,
    "directory-line": 64,
    "commit-line": 64,
    "commits-line": 64,
    "raw": 64,
    "directory-raw": 64,
    "filename-line-raw": 64,
    "filename-branch-line-raw": 64,
    "commit-raw": 64,
    "commits-raw": 64,
    "blame": 64,
    "directory-blame": 64,
    "commit-blame": 64,
    "commits-blame": 64,
    "raw-blame": 64,
    "directory-raw-blame": 64,
    "filename-raw-blame": 64
}

origins_and_bases = {
    "stash": {
        "default": "ssh-project",
        "configs": {
            "ssh-project": {
                "origin": "ssh://git@stash.mycompany.com:8080/PROJ/repo.git",
                "base": "https://stash.mycompany.com/projects/PROJ/repos/repo"
            },
            "ssh-user": {
                "origin": "ssh://git@stash.mycompany.com:8080/~someuser/repo.git",
                "base": "https://stash.mycompany.com/users/someuser/repos/repo"
            },
            "https-project-1": {
                "origin": "https://someuser@stash.mycompany.com/scm/proj/repo.git",
                "base": "https://stash.mycompany.com/projects/PROJ/repos/repo"
            },
            "https-user-1": {
                "origin": "https://someuser@stash.mycompany.com/scm/~someuser/repo.git",
                "base": "https://stash.mycompany.com/users/someuser/repos/repo"
            },
            "https-project-2": {
                "origin": "https://someuser@my.company.com/stash/scm/proj/repo.git",
                "base": "https://my.company.com/stash/projects/PROJ/repos/repo"
            },
            "https-user-2": {
                "origin": "https://someuser@my.company.com/stash/scm/~someuser/repo.git",
                "base": "https://my.company.com/stash/users/someuser/repos/repo"
            }
        }
    },
    "github": {
        "default": "ssh",
        "configs": {
            "ssh": {
                "origin": "git@github.com:user/repo.git",
                "base": "https://github.com/user/repo"
            },
            "https": {
                "origin": "https://github.com/user/repo.git",
                "base": "https://github.com/user/repo"
            },
            "svn": {
                "origin": "https://github.com/user/repo",
                "base": "https://github.com/user/repo"
            }
        }
    },
    "gitlab": {
        "default": "ssh",
        "configs": {
            "ssh": {
                "origin": "git@gitlab.com:user/repo.git",
                "base": "https://gitlab.com/user/repo"
            },
            "https": {
                "origin": "https://gitlab.com/user/repo.git",
                "base": "https://gitlab.com/user/repo"
            },
            "ssh-custom": {
                "origin": "git@gitlab.myorg.com/user/repo.git",
                "base": "https://gitlab.myorg.com/user/repo"
            },
            "https-custom": {
                "origin": "https://gitlab.myorg.com/user/repo.git",
                "base": "https://gitlab.myorg.com/user/repo"
            }
        }
    },
    "gitorious": {
        "default": "ssh",
        "configs": {
            "ssh": {
                "origin": "git@gitorious.org:project/repo.git",
                "base": "https://gitorious.org/project/repo"
            },
            "https": {
                "origin": "https://git.gitorious.org/project/repo.git",
                "base": "https://gitorious.org/project/repo"
            },
            "git": {
                "origin": "git://gitorious.org/project/repo",
                "base": "https://gitorious.org/project/repo"
            }
        }
    },
    "bitbucket": {
        "default": "ssh",
        "configs": {
            "ssh": {
                "origin": "git@bitbucket.org:project/repo.git",
                "base": "https://bitbucket.org/project/repo"
            },
            "https": {
                "origin": "https://user@bitbucket.org/project/repo.git",
                "base": "https://bitbucket.org/project/repo"
            }
        }
    }
}

# Define groups of tests; each group tests a different type of repository
test_groups = [
    {
        "name": "Origin URL tests",
        "type": "origins",
        "tests": {
            "stash-ssh-project": "/browse",
            "stash-ssh-user": "/browse",
            "stash-https-project-1": "/browse",
            "stash-https-user-1": "/browse",
            "github-ssh": "",
            "github-https": "",
            "github-svn": "",
            "gitlab-ssh": "/tree/master",
            "gitlab-https": "/tree/master",
            "gitlab-ssh-custom": "/tree/master",
            "gitlab-https-custom": "/tree/master",
            "gitorious-ssh": "",
            "gitorious-https": "",
            "gitorious-git": "",
            "bitbucket-ssh": "/src",
            "bitbucket-https": "/src"
        }
    },
    {
        "name": "Secondary Stash origin URL tests",
        "type": "origins",
        "env-setup": "os.putenv(\"TEST_STASH_URL_ROOT\", \"https://my.company.com/stash\")",
        "tests": {
            "stash-https-project-2": "/browse",
            "stash-https-user-2": "/browse"
        }
    },
    {
        "name": "Stash tests",
        "type": "general",
        "service": "stash",
        "env-setup": "os.putenv(\"TEST_STASH_URL_ROOT\", \"https://stash.mycompany.com\")",
        "tests": [
            {
                "run-error-tests": True,
                "expectations": {
                    "branch": "/browse?at=test1",
                    "tag": "/browse?at=1.0.0",
                    "directory": "/browse/foo/bar",
                    "directory-branch": "/browse/foo/bar?at=test1",
                    "directory-tag": "/browse/foo/bar?at=1.0.0",
                    "filename": "/browse/foo/bar/baz.ext",
                    "filename-branch": "/browse/foo/bar/baz.ext?at=test1",
                    "filename-tag": "/browse/foo/bar/baz.ext?at=1.0.0",
                    "filename-line": "/browse/foo/bar/baz.ext#5",
                    "filename-branch-line": "/browse/foo/bar/baz.ext?at=test1#5",
                    "commit": "/commits/092e8627fde84d5558c4429775d3498ec1ddce9a",
                    "commits": "/commits",
                    "commits-branch": "/commits?at=test1",
                    "commits-tag": "/commits?at=1.0.0",
                    "filename-raw": "/browse/foo/bar/baz.ext?raw",
                    "filename-branch-raw": "/browse/foo/bar/baz.ext?at=test1&raw",
                    "filename-blame": 64,
                    "filename-branch-blame": 64,
                    "filename-line-blame": 64,
                    "filename-branch-line-blame": 64
                }
            },
            {
                "filename": "baz.ext",
                "prefix-dir": "foo/bar",
                "expectations": {
                    "default": "/browse/foo/bar",
                    "branch": "/browse/foo/bar?at=test1",
                    "tag": "/browse/foo/bar?at=1.0.0",
                    "filename": "/browse/foo/bar/baz.ext",
                    "filename-branch": "/browse/foo/bar/baz.ext?at=test1",
                    "filename-tag": "/browse/foo/bar/baz.ext?at=1.0.0",
                    "filename-line": "/browse/foo/bar/baz.ext#5",
                    "filename-branch-line": "/browse/foo/bar/baz.ext?at=test1#5",
                    "commit": "/commits/092e8627fde84d5558c4429775d3498ec1ddce9a",
                    "commits": "/commits",
                    "commits-branch": "/commits?at=test1",
                    "commits-tag": "/commits?at=1.0.0",
                    "filename-raw": "/browse/foo/bar/baz.ext?raw",
                    "filename-branch-raw": "/browse/foo/bar/baz.ext?at=test1&raw"
                }
            },
            {
                "before": "git checkout test2",
                "expectations": {
                    "default": "/browse?at=test2",
                    "directory": "/browse/foo/bar?at=test2",
                    "filename": "/browse/foo/bar/baz.ext?at=test2",
                    "filename-line": "/browse/foo/bar/baz.ext?at=test2#5",
                    "commit": "/commits/092e8627fde84d5558c4429775d3498ec1ddce9a?at=test2",
                    "commits": "/commits?at=test2",
                    "filename-raw": "/browse/foo/bar/baz.ext?at=test2&raw"
                }
            }
        ]
    },
    {
        "name": "GitHub tests",
        "type": "general",
        "service": "github",
        "tests": [
            {
                "run-error-tests": True,
                "expectations": {
                    "branch": "/tree/test1",
                    "tag": "/tree/1.0.0",
                    "directory": "/tree/master/foo/bar",
                    "directory-branch": "/tree/test1/foo/bar",
                    "directory-tag": "/tree/1.0.0/foo/bar",
                    "filename": "/blob/master/foo/bar/baz.ext",
                    "filename-branch": "/blob/test1/foo/bar/baz.ext",
                    "filename-tag": "/blob/1.0.0/foo/bar/baz.ext",
                    "filename-line": "/blob/master/foo/bar/baz.ext#L5",
                    "filename-branch-line": "/blob/test1/foo/bar/baz.ext#L5",
                    "commit": "/commit/092e8627fde84d5558c4429775d3498ec1ddce9a",
                    "commits": "/commits/master",
                    "commits-branch": "/commits/test1",
                    "commits-tag": "/commits/1.0.0",
                    "filename-raw": "/raw/master/foo/bar/baz.ext",
                    "filename-branch-raw": "/raw/test1/foo/bar/baz.ext",
                    "filename-blame": "/blame/master/foo/bar/baz.ext",
                    "filename-branch-blame": "/blame/test1/foo/bar/baz.ext",
                    "filename-line-blame": "/blame/master/foo/bar/baz.ext#L5",
                    "filename-branch-line-blame": "/blame/test1/foo/bar/baz.ext#L5"
                }
            },
            {
                "filename": "baz.ext",
                "prefix-dir": "foo/bar",
                "expectations": {
                    "default": "/tree/master/foo/bar",
                    "branch": "/tree/test1/foo/bar",
                    "tag": "/tree/1.0.0/foo/bar",
                    "filename": "/blob/master/foo/bar/baz.ext",
                    "filename-branch": "/blob/test1/foo/bar/baz.ext",
                    "filename-tag": "/blob/1.0.0/foo/bar/baz.ext",
                    "filename-line": "/blob/master/foo/bar/baz.ext#L5",
                    "filename-branch-line": "/blob/test1/foo/bar/baz.ext#L5",
                    "commit": "/commit/092e8627fde84d5558c4429775d3498ec1ddce9a",
                    "commits": "/commits/master",
                    "commits-branch": "/commits/test1",
                    "commits-tag": "/commits/1.0.0",
                    "filename-raw": "/raw/master/foo/bar/baz.ext",
                    "filename-branch-raw": "/raw/test1/foo/bar/baz.ext"
                }
            },
            {
                "before": "git checkout test2",
                "expectations": {
                    "filename": "/blob/test2/foo/bar/baz.ext",
                    "filename-line": "/blob/test2/foo/bar/baz.ext#L5",
                    "commit": "/commit/092e8627fde84d5558c4429775d3498ec1ddce9a",
                    "commits": "/commits/test2",
                    "filename-raw": "/raw/test2/foo/bar/baz.ext"
                }
            }
        ]
    },
    {
        "name": "GitLab tests",
        "type": "general",
        "service": "gitlab",
        "tests": [
            {
                "run-error-tests": True,
                "expectations": {
                    "branch": "/tree/test1",
                    "tag": "/tree/1.0.0",
                    "directory": "/tree/master/foo/bar",
                    "directory-branch": "/tree/test1/foo/bar",
                    "directory-tag": "/tree/1.0.0/foo/bar",
                    "filename": "/blob/master/foo/bar/baz.ext",
                    "filename-branch": "/blob/test1/foo/bar/baz.ext",
                    "filename-tag": "/blob/1.0.0/foo/bar/baz.ext",
                    "filename-line": "/blob/master/foo/bar/baz.ext#L5",
                    "filename-branch-line": "/blob/test1/foo/bar/baz.ext#L5",
                    "commit": "/commit/092e8627fde84d5558c4429775d3498ec1ddce9a",
                    "commits": "/commits/master",
                    "commits-branch": "/commits/test1",
                    "commits-tag": "/commits/1.0.0",
                    "filename-raw": "/raw/master/foo/bar/baz.ext",
                    "filename-branch-raw": "/raw/test1/foo/bar/baz.ext",
                    "filename-blame": "/blame/master/foo/bar/baz.ext",
                    "filename-branch-blame": "/blame/test1/foo/bar/baz.ext",
                    "filename-line-blame": "/blame/master/foo/bar/baz.ext#L5",
                    "filename-branch-line-blame": "/blame/test1/foo/bar/baz.ext#L5"
                }
            },
            {
                "filename": "baz.ext",
                "prefix-dir": "foo/bar",
                "expectations": {
                    "default": "/tree/master/foo/bar",
                    "branch": "/tree/test1/foo/bar",
                    "tag": "/tree/1.0.0/foo/bar",
                    "filename": "/blob/master/foo/bar/baz.ext",
                    "filename-branch": "/blob/test1/foo/bar/baz.ext",
                    "filename-tag": "/blob/1.0.0/foo/bar/baz.ext",
                    "filename-line": "/blob/master/foo/bar/baz.ext#L5",
                    "filename-branch-line": "/blob/test1/foo/bar/baz.ext#L5",
                    "commit": "/commit/092e8627fde84d5558c4429775d3498ec1ddce9a",
                    "commits": "/commits/master",
                    "commits-branch": "/commits/test1",
                    "commits-tag": "/commits/1.0.0",
                    "filename-raw": "/raw/master/foo/bar/baz.ext",
                    "filename-branch-raw": "/raw/test1/foo/bar/baz.ext"
                }
            },
            {
                "before": "git checkout test2",
                "expectations": {
                    "filename": "/blob/test2/foo/bar/baz.ext",
                    "filename-line": "/blob/test2/foo/bar/baz.ext#L5",
                    "commit": "/commit/092e8627fde84d5558c4429775d3498ec1ddce9a",
                    "commits": "/commits/test2",
                    "filename-raw": "/raw/test2/foo/bar/baz.ext"
                }
            }
        ]
    },
    {
        "name": "Gitorious tests",
        "type": "general",
        "service": "gitorious",
        "tests": [
            {
                "run-error-tests": True,
                "expectations": {
                    "branch": "/source/test1",
                    "tag": "/source/1.0.0",
                    "directory": "/source/master:foo/bar",
                    "directory-branch": "/source/test1:foo/bar",
                    "directory-tag": "/source/1.0.0:foo/bar",
                    "filename": "/source/master:foo/bar/baz.ext",
                    "filename-branch": "/source/test1:foo/bar/baz.ext",
                    "filename-tag": "/source/1.0.0:foo/bar/baz.ext",
                    "filename-line": "/source/master:foo/bar/baz.ext#L5",
                    "filename-branch-line": "/source/test1:foo/bar/baz.ext#L5",
                    "commit": "/commit/092e8627fde84d5558c4429775d3498ec1ddce9a",
                    "commits": "/commits/master",
                    "commits-branch": "/commits/test1",
                    "commits-tag": "/commits/1.0.0",
                    "filename-raw": "/raw/master:foo/bar/baz.ext",
                    "filename-branch-raw": "/raw/test1:foo/bar/baz.ext",
                    "filename-blame": "/blame/master:foo/bar/baz.ext",
                    "filename-branch-blame": "/blame/test1:foo/bar/baz.ext",
                    "filename-line-blame": "/blame/master:foo/bar/baz.ext#L5",
                    "filename-branch-line-blame": "/blame/test1:foo/bar/baz.ext#L5"
                }
            },
            {
                "filename": "baz.ext",
                "prefix-dir": "foo/bar",
                "expectations": {
                    "default": "/source/master:foo/bar",
                    "branch": "/source/test1:foo/bar",
                    "tag": "/source/1.0.0:foo/bar",
                    "filename": "/source/master:foo/bar/baz.ext",
                    "filename-branch": "/source/test1:foo/bar/baz.ext",
                    "filename-tag": "/source/1.0.0:foo/bar/baz.ext",
                    "filename-line": "/source/master:foo/bar/baz.ext#L5",
                    "filename-branch-line": "/source/test1:foo/bar/baz.ext#L5",
                    "commit": "/commit/092e8627fde84d5558c4429775d3498ec1ddce9a",
                    "commits": "/commits/master",
                    "commits-branch": "/commits/test1",
                    "commits-tag": "/commits/1.0.0",
                    "filename-raw": "/raw/master:foo/bar/baz.ext",
                    "filename-branch-raw": "/raw/test1:foo/bar/baz.ext"
                }
            },
            {
                "before": "git checkout test2",
                "expectations": {
                    "filename": "/source/test2:foo/bar/baz.ext",
                    "filename-line": "/source/test2:foo/bar/baz.ext#L5",
                    "commit": "/commit/092e8627fde84d5558c4429775d3498ec1ddce9a",
                    "commits": "/commits/test2",
                    "filename-raw": "/raw/test2:foo/bar/baz.ext"
                }
            }
        ]
    },
    {
        "name": "Bitbucket tests",
        "type": "general",
        "service": "bitbucket",
        "tests": [
            {
                "run-error-tests": True,
                "expectations": {
                    "branch": "/src/test1/?at=test1",
                    "tag": "/src/1.0.0/?at=1.0.0",
                    "directory": "/src/master/foo/bar?at=master",
                    "directory-branch": "/src/test1/foo/bar?at=test1",
                    "directory-tag": "/src/1.0.0/foo/bar?at=1.0.0",
                    "filename": "/src/master/foo/bar/baz.ext?at=master",
                    "filename-branch": "/src/test1/foo/bar/baz.ext?at=test1",
                    "filename-tag": "/src/1.0.0/foo/bar/baz.ext?at=1.0.0",
                    "filename-line": "/src/master/foo/bar/baz.ext?at=master#cl-5",
                    "filename-branch-line": "/src/test1/foo/bar/baz.ext?at=test1#cl-5",
                    "commit": "/commits/092e8627fde84d5558c4429775d3498ec1ddce9a",
                    "commits": "/commits/branch/master",
                    "commits-branch": "/commits/branch/test1",
                    "commits-tag": "/commits/tag/1.0.0",
                    "filename-raw": "/raw/master/foo/bar/baz.ext?at=master",
                    "filename-branch-raw": "/raw/test1/foo/bar/baz.ext?at=test1",
                    "filename-blame": "/annotate/master/foo/bar/baz.ext?at=master",
                    "filename-branch-blame": "/annotate/test1/foo/bar/baz.ext?at=test1",
                    "filename-line-blame": "/annotate/master/foo/bar/baz.ext?at=master#cl-5",
                    "filename-branch-line-blame": "/annotate/test1/foo/bar/baz.ext?at=test1#cl-5"
                }
            },
            {
                "filename": "baz.ext",
                "prefix-dir": "foo/bar",
                "expectations": {
                    "default": "/src/master/foo/bar?at=master",
                    "branch": "/src/test1/foo/bar?at=test1",
                    "tag": "/src/1.0.0/foo/bar?at=1.0.0",
                    "filename": "/src/master/foo/bar/baz.ext?at=master",
                    "filename-branch": "/src/test1/foo/bar/baz.ext?at=test1",
                    "filename-tag": "/src/1.0.0/foo/bar/baz.ext?at=1.0.0",
                    "filename-line": "/src/master/foo/bar/baz.ext?at=master#cl-5",
                    "filename-branch-line": "/src/test1/foo/bar/baz.ext?at=test1#cl-5",
                    "commit": "/commits/092e8627fde84d5558c4429775d3498ec1ddce9a",
                    "commits": "/commits/branch/master",
                    "commits-branch": "/commits/branch/test1",
                    "commits-tag": "/commits/tag/1.0.0",
                    "filename-raw": "/raw/master/foo/bar/baz.ext?at=master",
                    "filename-branch-raw": "/raw/test1/foo/bar/baz.ext?at=test1"
                }
            },
            {
                "before": "git checkout test2",
                "expectations": {
                    "filename": "/src/test2/foo/bar/baz.ext?at=test2",
                    "filename-line": "/src/test2/foo/bar/baz.ext?at=test2#cl-5",
                    "commit": "/commits/092e8627fde84d5558c4429775d3498ec1ddce9a",
                    "commits": "/commits/branch/test2",
                    "filename-raw": "/raw/test2/foo/bar/baz.ext?at=test2"
                }
            }
        ]
    }
]

# Helper function to suppress output if quiet mode is enabled
def out(msg):
    if not args.quiet:
        print msg

# Suppress most command output if quiet mode is enabled
to_dev_null = " &>/dev/null" if args.quiet else ""

# Set up some variables to quantify the test results
total = 0
successes = 0
failures = 0

# Set up the test repository
print "setting up tests..."
subprocess.call("git init testrepo" + to_dev_null, shell=True)
subprocess.call("cd testrepo; git remote add origin this-is-fake" + to_dev_null, shell=True)
subprocess.call("cd testrepo; mkdir -p foo/bar" + to_dev_null, shell=True)
subprocess.call("cd testrepo; touch foo/bar/baz.ext" + to_dev_null, shell=True)
subprocess.call("cd testrepo; git add foo" + to_dev_null, shell=True)
subprocess.call("cd testrepo; git commit -m \"init\"" + to_dev_null, shell=True)
subprocess.call("cd testrepo; git checkout -b test1" + to_dev_null, shell=True)
subprocess.call("cd testrepo; git checkout -b test2" + to_dev_null, shell=True)
subprocess.call("cd testrepo; git tag -a 1.0.0 -m \"1.0.0\"" + to_dev_null, shell=True)

# Helper function to set the origin URL
def set_origin(origin_url):
    setup_cmd = "cd testrepo; git remote set-url origin {0}; git checkout master {1}".format(origin_url, to_dev_null)
    subprocess.call(setup_cmd, shell=True)

# Run the test case and handle the output
def run_test(test_args, expected_output, prefix=""):
    test = DEFAULT_COMMAND_BASE + test_args
    prefix_command = "cd testrepo; " + prefix
    command = "{0} &>/dev/null; {1}".format(prefix_command, test)

    out("running \"{0}\"...".format(prefix_command))
    out("testing \"{0}\"...".format(test))

    output = ""
    exit_code = 0
    try:
        output = subprocess.check_output(command, shell=True).rstrip()
    except subprocess.CalledProcessError, e:
        output = e.output
        exit_code = e.returncode

    # Check the output to see if the test passed or failed, and print the result
    if output == expected_output or exit_code == expectation:
        out(" > \033[92mpass\033[0m")
        success = True
    else:
        if args.quiet:
            location = ""
            if prefix != "":
                location = " in {0}".format(prefix)
            print "testing \"{0}\"{1}...".format(test, location)
        print " > \033[91mFAIL\033[0m\n > expected: {0}\n > actual:   {1}".format(expected_output, output)
        success = False
    out("")

    return success

# Loop over each defined group of tests
for group in test_groups:
    # Keep track of test stats for each group
    group_total = 0
    group_successes = 0
    group_failures = 0

    print "\033[93m===== " + group["name"] + " =====\033[0m"

    # Run environment setup if requested to set variables for custom domains
    if "env-setup" in group:
        out("running " + group["env-setup"])
        eval(group["env-setup"])

    if group["type"] == "origins":
        # Test all origin URL variations
        for definition, expectation in group["tests"].iteritems():
            def_arr = definition.split("-", 1)
            service = def_arr[0]
            origin = def_arr[1]

            origin_def = origins_and_bases[service]["configs"][origin]
            origin_url = origin_def["origin"]
            set_origin(origin_url)
            expected = origin_def["base"] + expectation

            group_total += 1
            success = run_test(test_definitions["default"], expected)
            if success:
                group_successes += 1
            else:
                group_failures += 1
    else:
        service = group["service"]
        default_origin = origins_and_bases[service]["default"]
        origin_info = origins_and_bases[service]["configs"][default_origin]
        set_origin(origin_info["origin"])
        # Handle each group of test cases for this test group
        for subgroup in group["tests"]:
            # Run any setup tasks for the subgroup
            if "before" in subgroup:
                out("running " + subgroup["before"])
                subprocess.call("cd testrepo; " + subgroup["before"] + to_dev_null, shell=True)

            # Default the directory and filename if they haven't been specified
            directory = subgroup["directory"] if "directory" in subgroup else "foo/bar/"
            filename = subgroup["filename"] if "filename" in subgroup else "foo/bar/baz.ext"

            # If requested, add the test cases that are expected to always return errors
            expectations = subgroup["expectations"]
            if "run-error-tests" in subgroup:
                expectations.update(error_tests)

            # Loop over test cases to prepare and run them
            for case, expectation in expectations.iteritems():
                # Get the command arguments and expected result for the test case
                test = test_definitions[case]
                expected_output = "{0}{1}".format(origin_info["base"], expectation)
                group_total += 1
                prefix = ""

                if "prefix-dir" in subgroup:
                    prefix = "cd " + subgroup["prefix-dir"]

                # Inject the correct directory/filename into the arguments if required
                if "directory" in case:
                    test = test.format(directory)
                elif "filename" in case:
                    test = test.format(filename)

                # Finally, execute the test case
                success = run_test(test, expected_output, prefix)
                if success:
                    group_successes += 1
                else:
                    group_failures += 1

    print "GROUP SUMMARY: {0} total tests, {1} passed, {2} failed\n".format(group_total, group_successes, group_failures)

    # Aggregate the group totals for a final summary
    total += group_total
    successes += group_successes
    failures += group_failures

# Delete the test repo and print the test summary
out("cleaning up...")
subprocess.call("rm -rf testrepo" + to_dev_null, shell=True)

print "\nTOTAL SUMMARY: {0} total tests, {1} passed, {2} failed\n".format(total, successes, failures)
