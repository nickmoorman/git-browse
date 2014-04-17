#!/usr/bin/env python

"""test-git-browse.py, v0.1.3: Custom unit tests for git-browse Bash script"""

__author__ = "Nick Sawyer <nick@nicksawyer.net>"

import os
import subprocess

os.environ["TEST_STASH_HOSTNAME"] = "stash.mycompany.com"
os.environ["TEST_STASH_URL_ROOT"] = "https://stash.mycompany.com"

test_groups = [
    {
        "name": "Stash tests (SSH remote)",
        "expected_base": "https://stash.mycompany.com/projects/PROJ/repos/repo",
        "command_base": "git-browse --url-only ",
        "tests": [
            {
                "cases": [
                    {
                        "arguments": "",
                        "expected": "/browse",
                        "before": "git checkout master"
                    },
                    {
                        "arguments": "foo/bar/baz.ext",
                        "expected": "/browse/foo/bar/baz.ext"
                    },
                    {
                        "arguments": "foo/bar/baz.ext --ref=test1",
                        "expected": "/browse/foo/bar/baz.ext?at=test1"
                    },
                    {
                        "arguments": "--ref=test1 foo/bar/baz.ext",
                        "expected": "/browse/foo/bar/baz.ext?at=test1"
                    },
                    {
                        "arguments": "foo/bar/baz.ext --line=25",
                        "expected": "/browse/foo/bar/baz.ext#25"
                    },
                    {
                        "arguments": "foo/bar/baz.ext --ref=test1 --line=25",
                        "expected": "/browse/foo/bar/baz.ext?at=test1#25"
                    },
                    {
                        "arguments": "a78cd8e",
                        "expected": "/commits/a78cd8e"
                    },
                    {
                        "arguments": "--commits",
                        "expected": "/commits"
                    },
                    {
                        "arguments": "--ref=test1",
                        "expected": "/browse?at=test1"
                    },
                    {
                        "arguments": "--commits --ref=test1",
                        "expected": "/commits?at=test1"
                    },
                    {
                        "arguments": "--ref=test1 --commits",
                        "expected": "/commits?at=test1"
                    }
                ]
            },
            {
                "before": "cd foo/bar",
                "cases": [
                    {
                        "arguments": "",
                        "expected": "/browse/foo/bar"
                    },
                    {
                        "arguments": "baz.ext",
                        "expected": "/browse/foo/bar/baz.ext"
                    },
                    {
                        "arguments": "baz.ext --ref=test1",
                        "expected": "/browse/foo/bar/baz.ext?at=test1"
                    },
                    {
                        "arguments": "--ref=test1 baz.ext",
                        "expected": "/browse/foo/bar/baz.ext?at=test1"
                    },
                    {
                        "arguments": "baz.ext --line=25",
                        "expected": "/browse/foo/bar/baz.ext#25"
                    },
                    {
                        "arguments": "baz.ext --ref=test1 --line=25",
                        "expected": "/browse/foo/bar/baz.ext?at=test1#25"
                    },
                    {
                        "arguments": "a78cd8e",
                        "expected": "/commits/a78cd8e"
                    },
                    {
                        "arguments": "--commits",
                        "expected": "/commits"
                    },
                    {
                        "arguments": "--ref=test1",
                        "expected": "/browse/foo/bar?at=test1"
                    },
                    {
                        "arguments": "--commits --ref=test1",
                        "expected": "/commits?at=test1"
                    },
                    {
                        "arguments": "--ref=test1 --commits",
                        "expected": "/commits?at=test1"
                    },
                ]
            },
            {
                "cases": [
                    {
                        "arguments": "foo/bar/baz.ext",
                        "expected": "/browse/foo/bar/baz.ext?at=test2",
                        "before": "git checkout test2"
                    },
                    {
                        "arguments": "foo/bar/baz.ext --line=25",
                        "expected": "/browse/foo/bar/baz.ext?at=test2#25"
                    },
                    {
                        "arguments": "a78cd8e",
                        "expected": "/commits/a78cd8e?at=test2"
                    },
                    {
                        "arguments": "--commits",
                        "expected": "/commits?at=test2"
                    }
                ]
            }
        ]
    },
    {
        "name": "Stash tests (HTTPS remote)",
        "setup": "cd testrepo; git remote set-url origin https://someuser@stash.mycompany.com/scm/proj/repo.git",
        "expected_base": "https://stash.mycompany.com/projects/PROJ/repos/repo",
        "command_base": "git-browse --url-only ",
        "tests": [
            {
                "cases": [
                    {
                        "arguments": "",
                        "expected": "/browse",
                        "before": "git checkout master"
                    },
                    {
                        "arguments": "foo/bar/baz.ext",
                        "expected": "/browse/foo/bar/baz.ext"
                    },
                    {
                        "arguments": "foo/bar/baz.ext --ref=test1",
                        "expected": "/browse/foo/bar/baz.ext?at=test1"
                    }
                ]
            }
        ]
    },
    {
        "name": "GitHub tests (SSH remote)",
        "setup": "cd testrepo; git remote set-url origin git@github.com:user/repo.git",
        "expected_base": "https://github.com/user/repo",
        "command_base": "git-browse --url-only ",
        "tests": [
            {
                "cases": [
                    {
                        "arguments": "",
                        "expected": "",
                        "before": "git checkout master"
                    },
                    {
                        "arguments": "foo/bar/baz.ext",
                        "expected": "/blob/master/foo/bar/baz.ext"
                    },
                    {
                        "arguments": "foo/bar/baz.ext --ref=test1",
                        "expected": "/blob/test1/foo/bar/baz.ext"
                    },
                    {
                        "arguments": "--ref=test1 foo/bar/baz.ext",
                        "expected": "/blob/test1/foo/bar/baz.ext"
                    },
                    {
                        "arguments": "foo/bar/baz.ext --line=25",
                        "expected": "/blob/master/foo/bar/baz.ext#L25"
                    },
                    {
                        "arguments": "foo/bar/baz.ext --ref=test1 --line=25",
                        "expected": "/blob/test1/foo/bar/baz.ext#L25"
                    },
                    {
                        "arguments": "a78cd8e",
                        "expected": "/commit/a78cd8e"
                    },
                    {
                        "arguments": "--commits",
                        "expected": "/commits/master"
                    },
                    {
                        "arguments": "--ref=test1",
                        "expected": "/tree/test1"
                    },
                    {
                        "arguments": "--commits --ref=test1",
                        "expected": "/commits/test1"
                    },
                    {
                        "arguments": "--ref=test1 --commits",
                        "expected": "/commits/test1"
                    }
                ]
            },
            {
                "before": "cd foo/bar",
                "cases": [
                    {
                        "arguments": "",
                        "expected": "/tree/master/foo/bar"
                    },
                    {
                        "arguments": "baz.ext",
                        "expected": "/blob/master/foo/bar/baz.ext"
                    },
                    {
                        "arguments": "baz.ext --ref=test1",
                        "expected": "/blob/test1/foo/bar/baz.ext"
                    },
                    {
                        "arguments": "--ref=test1 baz.ext",
                        "expected": "/blob/test1/foo/bar/baz.ext"
                    },
                    {
                        "arguments": "baz.ext --line=25",
                        "expected": "/blob/master/foo/bar/baz.ext#L25"
                    },
                    {
                        "arguments": "baz.ext --ref=test1 --line=25",
                        "expected": "/blob/test1/foo/bar/baz.ext#L25"
                    },
                    {
                        "arguments": "a78cd8e",
                        "expected": "/commit/a78cd8e"
                    },
                    {
                        "arguments": "--commits",
                        "expected": "/commits/master"
                    },
                    {
                        "arguments": "--ref=test1",
                        "expected": "/tree/test1/foo/bar"
                    },
                    {
                        "arguments": "--commits --ref=test1",
                        "expected": "/commits/test1"
                    },
                    {
                        "arguments": "--ref=test1 --commits",
                        "expected": "/commits/test1"
                    },
                ]
            },
            {
                "cases": [
                    {
                        "arguments": "foo/bar/baz.ext",
                        "expected": "/blob/test2/foo/bar/baz.ext",
                        "before": "git checkout test2"
                    },
                    {
                        "arguments": "foo/bar/baz.ext --line=25",
                        "expected": "/blob/test2/foo/bar/baz.ext#L25"
                    },
                    {
                        "arguments": "a78cd8e",
                        "expected": "/commit/a78cd8e"
                    },
                    {
                        "arguments": "--commits",
                        "expected": "/commits/test2"
                    }
                ]
            }
        ]
    },
    {
        "name": "GitHub tests (HTTPS remote)",
        "setup": "cd testrepo; git remote set-url origin https://github.com/user/repo.git",
        "expected_base": "https://github.com/user/repo",
        "command_base": "git-browse --url-only ",
        "tests": [
            {
                "cases": [
                    {
                        "arguments": "",
                        "expected": "",
                        "before": "git checkout master"
                    },
                    {
                        "arguments": "foo/bar/baz.ext",
                        "expected": "/blob/master/foo/bar/baz.ext"
                    },
                    {
                        "arguments": "foo/bar/baz.ext --ref=test1",
                        "expected": "/blob/test1/foo/bar/baz.ext"
                    }
                ]
            }
        ]
    },
]

total = 0
successes = 0
failures = 0

print "setting up tests..."
subprocess.call("git init testrepo", shell=True)
subprocess.call("cd testrepo; git remote add origin ssh://git@stash.mycompany.com:8080/PROJ/repo.git", shell=True)
subprocess.call("cd testrepo; mkdir -p foo/bar", shell=True)
subprocess.call("cd testrepo; touch foo/bar/baz.ext", shell=True)
subprocess.call("cd testrepo; git add foo", shell=True)
subprocess.call("cd testrepo; git commit -m \"init\"", shell=True)
subprocess.call("cd testrepo; git checkout -b test1", shell=True)
subprocess.call("cd testrepo; git checkout -b test2", shell=True)

for group in test_groups:
    group_total = 0
    group_successes = 0
    group_failures = 0
    print "\033[93m===== " + group["name"] + " =====\033[0m"
    if "setup" in group:
        print "running test group setup commands..."
        subprocess.call(group["setup"], shell=True)

    for subgroup in group["tests"]:
        for test in subgroup["cases"]:
            group_total += 1
            c = ""
            before = "cd testrepo; "

            if "before" in subgroup:
                before += subgroup["before"]
            elif "before" in test:
                before += test["before"]

            print "running \"{0}\"...".format(before)
            c += "{0} &>/dev/null; ".format(before)
            c += "{0}{1}".format(group["command_base"], test["arguments"])

            print "testing \"{0}{1}\"...".format(group["command_base"], test["arguments"])
            t = subprocess.check_output(c, shell=True).rstrip()
            if t == "{0}{1}".format(group["expected_base"], test["expected"]):
                print " > \033[92mpass\033[0m"
                group_successes += 1
            else:
                print " > \033[91mFAIL\033[0m\n > expected: {0}{1}\n > actual:   {2}".format(group["expected_base"], test["expected"], t)
                group_failures += 1
            print ""

    print "GROUP SUMMARY: {0} total tests, {1} passed, {2} failed\n".format(group_total, group_successes, group_failures)

    total += group_total
    successes += group_successes
    failures += group_failures

print "cleaning up..."
subprocess.call("rm -rf testrepo", shell=True)

print "\nTOTAL SUMMARY: {0} total tests, {1} passed, {2} failed\n".format(total, successes, failures)
