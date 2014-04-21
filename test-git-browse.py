#!/usr/bin/env python

"""test-git-browse.py, v0.1.4: Custom unit tests for git-browse Bash script"""

__author__ = "Nick Sawyer <nick@nicksawyer.net>"

import os
import subprocess

# Set some variables in the environment for building Stash URLs
os.environ["TEST_STASH_URL_ROOT"] = "https://stash.mycompany.com"
os.environ["TEST_GITLAB_URL_ROOT"] = "https://gitlab.myorg.com"

# Define the different argument combinations to test
test_definitions = {
    "default": "",
    "filename": "{0}",
    "filename-ref": "{0} --ref=test1",
    "ref-filename": "--ref=test1 {0}",
    "filename-line": "{0} --line=25",
    "filename-ref-line": "{0} --ref=test1 --line=25",
    "commit": "a78cd8e",
    "commits": "--commits",
    "ref": "--ref=test1",
    "commits-ref": "--commits --ref=test1",
    "ref-commits": "--ref=test1 --commits"
}

# Define groups of tests; each group tests a different type of repository
test_groups = [
    {
        "name": "Stash tests (SSH remote)",
        "expected_base": "https://stash.mycompany.com/projects/PROJ/repos/repo",
        "command_base": "git-browse --url-only ",
        "tests": [
            {
                "expectations": {
                    "default": "/browse",
                    "filename": "/browse/foo/bar/baz.ext",
                    "filename-ref": "/browse/foo/bar/baz.ext?at=test1",
                    "ref-filename": "/browse/foo/bar/baz.ext?at=test1",
                    "filename-line": "/browse/foo/bar/baz.ext#25",
                    "filename-ref-line": "/browse/foo/bar/baz.ext?at=test1#25",
                    "commit": "/commits/a78cd8e",
                    "commits": "/commits",
                    "ref": "/browse?at=test1",
                    "commits-ref": "/commits?at=test1",
                    "ref-commits": "/commits?at=test1"
                }
            },
            {
                "filename": "baz.ext",
                "prefix-command": "cd foo/bar",
                "expectations": {
                    "default": "/browse/foo/bar",
                    "filename": "/browse/foo/bar/baz.ext",
                    "filename-ref": "/browse/foo/bar/baz.ext?at=test1",
                    "ref-filename": "/browse/foo/bar/baz.ext?at=test1",
                    "filename-line": "/browse/foo/bar/baz.ext#25",
                    "filename-ref-line": "/browse/foo/bar/baz.ext?at=test1#25",
                    "commit": "/commits/a78cd8e",
                    "commits": "/commits",
                    "ref": "/browse/foo/bar?at=test1",
                    "commits-ref": "/commits?at=test1",
                    "ref-commits": "/commits?at=test1"
                }
            },
            {
                "before": "git checkout test2",
                "expectations": {
                    "filename": "/browse/foo/bar/baz.ext?at=test2",
                    "filename-line": "/browse/foo/bar/baz.ext?at=test2#25",
                    "commit": "/commits/a78cd8e?at=test2",
                    "commits": "/commits?at=test2"
                }
            }
        ]
    },
    {
        "name": "Stash tests (HTTPS remote)",
        "setup": "cd testrepo; git remote set-url origin https://someuser@stash.mycompany.com/scm/proj/repo.git; git checkout master",
        "expected_base": "https://stash.mycompany.com/projects/PROJ/repos/repo",
        "command_base": "git-browse --url-only ",
        "tests": [
            {
                "expectations": {
                    "default": "/browse",
                    "filename": "/browse/foo/bar/baz.ext",
                    "filename-ref": "/browse/foo/bar/baz.ext?at=test1"
                }
            }
        ]
    },
    {
        "name": "GitHub tests (SSH remote)",
        "setup": "cd testrepo; git remote set-url origin git@github.com:user/repo.git; git checkout master",
        "expected_base": "https://github.com/user/repo",
        "command_base": "git-browse --url-only ",
        "tests": [
            {
                "expectations": {
                    "default": "",
                    "filename": "/blob/master/foo/bar/baz.ext",
                    "filename-ref": "/blob/test1/foo/bar/baz.ext",
                    "ref-filename": "/blob/test1/foo/bar/baz.ext",
                    "filename-line": "/blob/master/foo/bar/baz.ext#L25",
                    "filename-ref-line": "/blob/test1/foo/bar/baz.ext#L25",
                    "commit": "/commit/a78cd8e",
                    "commits": "/commits/master",
                    "ref": "/tree/test1",
                    "commits-ref": "/commits/test1",
                    "ref-commits": "/commits/test1"
                }
            },
            {
                "filename": "baz.ext",
                "prefix-command": "cd foo/bar",
                "expectations": {
                    "default": "/tree/master/foo/bar",
                    "filename": "/blob/master/foo/bar/baz.ext",
                    "filename-ref": "/blob/test1/foo/bar/baz.ext",
                    "ref-filename": "/blob/test1/foo/bar/baz.ext",
                    "filename-line": "/blob/master/foo/bar/baz.ext#L25",
                    "filename-ref-line": "/blob/test1/foo/bar/baz.ext#L25",
                    "commit": "/commit/a78cd8e",
                    "commits": "/commits/master",
                    "ref": "/tree/test1/foo/bar",
                    "commits-ref": "/commits/test1",
                    "ref-commits": "/commits/test1"
                }
            },
            {
                "before": "git checkout test2",
                "expectations": {
                    "filename": "/blob/test2/foo/bar/baz.ext",
                    "filename-line": "/blob/test2/foo/bar/baz.ext#L25",
                    "commit": "/commit/a78cd8e",
                    "commits": "/commits/test2"
                }
            }
        ]
    },
    {
        "name": "GitHub tests (HTTPS remote)",
        "setup": "cd testrepo; git remote set-url origin https://github.com/user/repo.git; git checkout master",
        "expected_base": "https://github.com/user/repo",
        "command_base": "git-browse --url-only ",
        "tests": [
            {
                "expectations": {
                    "default": "",
                    "filename": "/blob/master/foo/bar/baz.ext",
                    "filename-ref": "/blob/test1/foo/bar/baz.ext"
                }
            }
        ]
    },
    {
        "name": "GitLab tests (SSH remote)",
        "setup": "cd testrepo; git remote set-url origin git@gitlab.com:user/repo.git; git checkout master",
        "expected_base": "https://gitlab.com/user/repo",
        "command_base": "git-browse --url-only ",
        "tests": [
            {
                "expectations": {
                    "default": "/tree/master",
                    "filename": "/blob/master/foo/bar/baz.ext",
                    "filename-ref": "/blob/test1/foo/bar/baz.ext",
                    "ref-filename": "/blob/test1/foo/bar/baz.ext",
                    "filename-line": "/blob/master/foo/bar/baz.ext#L25",
                    "filename-ref-line": "/blob/test1/foo/bar/baz.ext#L25",
                    "commit": "/commit/a78cd8e",
                    "commits": "/commits/master",
                    "ref": "/tree/test1",
                    "commits-ref": "/commits/test1",
                    "ref-commits": "/commits/test1"
                }
            },
            {
                "filename": "baz.ext",
                "prefix-command": "cd foo/bar",
                "expectations": {
                    "default": "/tree/master/foo/bar",
                    "filename": "/blob/master/foo/bar/baz.ext",
                    "filename-ref": "/blob/test1/foo/bar/baz.ext",
                    "ref-filename": "/blob/test1/foo/bar/baz.ext",
                    "filename-line": "/blob/master/foo/bar/baz.ext#L25",
                    "filename-ref-line": "/blob/test1/foo/bar/baz.ext#L25",
                    "commit": "/commit/a78cd8e",
                    "commits": "/commits/master",
                    "ref": "/tree/test1/foo/bar",
                    "commits-ref": "/commits/test1",
                    "ref-commits": "/commits/test1"
                }
            },
            {
                "before": "git checkout test2",
                "expectations": {
                    "filename": "/blob/test2/foo/bar/baz.ext",
                    "filename-line": "/blob/test2/foo/bar/baz.ext#L25",
                    "commit": "/commit/a78cd8e",
                    "commits": "/commits/test2"
                }
            }
        ]
    },
    {
        "name": "GitLab tests (HTTPS remote)",
        "setup": "cd testrepo; git remote set-url origin https://gitlab.com/user/repo.git; git checkout master",
        "expected_base": "https://gitlab.com/user/repo",
        "command_base": "git-browse --url-only ",
        "tests": [
            {
                "expectations": {
                    "default": "/tree/master",
                    "filename": "/blob/master/foo/bar/baz.ext",
                    "filename-ref": "/blob/test1/foo/bar/baz.ext"
                }
            }
        ]
    },
    {
        "name": "GitLab tests (SSH remote, custom domain)",
        "setup": "cd testrepo; git remote set-url origin git@gitlab.myorg.com/user/repo.git; git checkout master",
        "expected_base": "https://gitlab.myorg.com/user/repo",
        "command_base": "git-browse --url-only ",
        "tests": [
            {
                "expectations": {
                    "default": "/tree/master",
                    "filename": "/blob/master/foo/bar/baz.ext",
                    "filename-ref": "/blob/test1/foo/bar/baz.ext"
                }
            }
        ]
    },
    {
        "name": "GitLab tests (HTTPS remote, custom domain)",
        "setup": "cd testrepo; git remote set-url origin https://gitlab.myorg.com/user/repo.git; git checkout master",
        "expected_base": "https://gitlab.myorg.com/user/repo",
        "command_base": "git-browse --url-only ",
        "tests": [
            {
                "expectations": {
                    "default": "/tree/master",
                    "filename": "/blob/master/foo/bar/baz.ext",
                    "filename-ref": "/blob/test1/foo/bar/baz.ext"
                }
            }
        ]
    }
]

# Set up some variables to quantify the test results
total = 0
successes = 0
failures = 0

# Set up the test repository
print "setting up tests..."
subprocess.call("git init testrepo", shell=True)
subprocess.call("cd testrepo; git remote add origin ssh://git@stash.mycompany.com:8080/PROJ/repo.git", shell=True)
subprocess.call("cd testrepo; mkdir -p foo/bar", shell=True)
subprocess.call("cd testrepo; touch foo/bar/baz.ext", shell=True)
subprocess.call("cd testrepo; git add foo", shell=True)
subprocess.call("cd testrepo; git commit -m \"init\"", shell=True)
subprocess.call("cd testrepo; git checkout -b test1", shell=True)
subprocess.call("cd testrepo; git checkout -b test2", shell=True)
subprocess.call("cd testrepo; git checkout master", shell=True)

# Loop over each defined group of tests
for group in test_groups:
    # Keep track of test stats for each group
    group_total = 0
    group_successes = 0
    group_failures = 0

    print "\033[93m===== " + group["name"] + " =====\033[0m"

    # If there are any setup steps for this test group, run them
    if "setup" in group:
        print "running test group setup commands..."
        subprocess.call(group["setup"], shell=True)

    # Handle each group of test cases for this test group
    for subgroup in group["tests"]:
        # Run any setup tasks for the subgroup
        if "before" in subgroup:
            print "running " + subgroup["before"]
            subprocess.call("cd testrepo; " + subgroup["before"], shell=True)

        # Default the filename if one hasn't been specified
        filename = subgroup["filename"] if "filename" in subgroup else "foo/bar/baz.ext"
        for case, expectation in subgroup["expectations"].iteritems():
            # Get the command arguments and expected result for the test case
            test = test_definitions[case]
            expected_output = group["expected_base"] + expectation
            group_total += 1
            prefix = "cd testrepo; "

            if "prefix-command" in subgroup:
                prefix += subgroup["prefix-command"]

            # Inject the correct filename into the arguments if required
            if "filename" in case:
                test = test.format(filename)

            # Finally, execute the test case
            test = group["command_base"] + test
            cmd = "{0} &>/dev/null; {1}".format(prefix, test)

            print "running \"{0}\"...".format(prefix)
            print "testing \"{0}\"...".format(test)
            output = subprocess.check_output(cmd, shell=True).rstrip()
            # Check the output to see if the test passed or failed, and print the result
            if output == expected_output:
                print " > \033[92mpass\033[0m"
                group_successes += 1
            else:
                print " > \033[91mFAIL\033[0m\n > expected: {0}\n > actual:   {1}".format(expected_output, output)
                group_failures += 1
            print ""

    print "GROUP SUMMARY: {0} total tests, {1} passed, {2} failed\n".format(group_total, group_successes, group_failures)

    # Aggregate the group totals for a final summary
    total += group_total
    successes += group_successes
    failures += group_failures

# Delete the test repo and print the test summary
print "cleaning up..."
subprocess.call("rm -rf testrepo", shell=True)

print "\nTOTAL SUMMARY: {0} total tests, {1} passed, {2} failed\n".format(total, successes, failures)
