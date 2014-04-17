#!/usr/bin/env python

"""test-git-browse.py, v1.0.0: Custom unit tests for git-browse Bash script"""

__author__ = "Nick Sawyer <nick@nicksawyer.net>"

import os
import subprocess

os.environ["TEST_STASH_HOSTNAME"] = "stash.mycompany.com"
os.environ["TEST_STASH_URL_ROOT"] = "https://stash.mycompany.com"

test_groups = [
    {
        "setup": "git init testrepo; cd testrepo; git remote add origin ssh://git@stash.mycompany.com:8080/PROJ/repo.git; mkdir -p foo/bar; touch foo/bar/baz.ext; git add foo; git commit -m \"init\"; git checkout -b test1; git checkout -b test2",
        "cleanup": "rm -rf testrepo",
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
    }
]

total = 0
successes = 0
failures = 0

for group in test_groups:
    if "setup" in group:
        print "setting up tests..."
        subprocess.call(group["setup"], shell=True)

    for subgroup in group["tests"]:
        for test in subgroup["cases"]:
            total += 1
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
            #subprocess.call(c, shell=True)
            t = subprocess.check_output(c, shell=True).rstrip()
            if t == "{0}{1}".format(group["expected_base"], test["expected"]):
                print " > pass"
                successes += 1
            else:
                print " > FAIL\n > expected: {0}{1}\n > actual:   {2}".format(group["expected_base"], test["expected"], t)
                failures += 1
            print ""

    if "cleanup" in group:
        print "cleaning up..."
        subprocess.call(group["cleanup"], shell=True)

print "SUMMARY: {0} total tests, {1} passed, {2} failed\n".format(total, successes, failures)
