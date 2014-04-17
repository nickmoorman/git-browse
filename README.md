# git-browse

`git-browse` is a useful tool that allows developers to easily share the URL to a particular file or directory in popular Git hosting solutions.  It's a simple bash script that can be run against almost any Git repository, and it constructs the URL for the requested resource and opens it in the user's default browser.

`git-browse` currently supports:

- [GitHub](https://github.com/)
- [Atlassian Stash](https://www.atlassian.com/software/stash)

Future plans on the roadmap include:

- Support for pull request URLs
- Possible support for GitLab, Gitorious, and BitBucket

## Installation & Setup
Currently, the easiest way to install this script on your machine is to set up a symlink to the script in a directory that's on your path.  If you don't have a good place for something like this already, I recommend creating a `bin` directory in your home directory, and then adding it to your path by including something like this (before `PATH` is exported) in your `.bashrc/.bash_profile`:

```
PATH=${HOME}/bin:${PATH}
```

After that, simply create the symlink(s).

```
$ cd ~/bin
$ ln -s /path/to/git-browse/git-browse .
$ ln -s /path/to/git-browse/test-git-browse.py . # optional
```

For the script to automatically link to the head that you have checked out, you'll need to install the [Git completion Bash script](https://github.com/git/git/blob/master/contrib/completion/git-completion.bash) if it's not already available on your system.  This can be done with [Homebrew](https://github.com/bobthecow/git-flow-completion/wiki/Install-Bash-git-completion) if you prefer that route.  Once this is installed, you'll need to copy the [sample configuration file](https://github.com/nickmoorman/git-browse/blob/master/.gitbrowse.sample) to `~/.gitbrowse` and update the path to your Git completion script accordingly.  This will allow the `git-browse` script to find it.

## Usage
Let's jump right into some examples to demonstrate what it can do. (Note: a usage summary is available at any time by running `git-browse --help`).

### The Basics
Open current directory:

```
nick@isis:~/dev/somestashrepo (master)$ git-browse
Opening 'https://stash.mycompany.com/projects/PROJ/repos/somestashrepo/browse'...
```

```
nick@isis:~/dev/somegithubrepo (master)$ git-browse
Opening 'https://github.com/someuser/somegithubrepo'...
```

Open a sub-directory:

```
nick@isis:~/dev/somestashrepo (master)$ git-browse foo/bar
Opening 'https://stash.mycompany.com/projects/PROJ/repos/somestashrepo/browse/foo/bar'...
```

```
nick@isis:~/dev/somegithubrepo (master)$ git-browse foo/bar
Opening 'https://github.com/someuser/somegithubrepo/tree/master/foo/bar'...
```

Open a file:

```
nick@isis:~/dev/somestashrepo (master)$ git-browse foo/bar/baz.ext
Opening 'https://stash.mycompany.com/projects/PROJ/repos/somestashrepo/browse/foo/bar/baz.ext'...
```

```
nick@isis:~/dev/somegithubrepo (master)$ git-browse foo/bar/baz.ext
Opening 'https://github.com/someuser/somegithubrepo/blob/master/foo/bar/baz.ext'...
```

These commands also work inside sub-directories!

```
nick@isis:~/dev/somestashrepo/foo/bar (master)$ git-browse
Opening 'https://stash.mycompany.com/projects/PROJ/repos/somestashrepo/browse/foo/bar'...
```

```
nick@isis:~/dev/somestashrepo/foo/bar (master)$ git-browse baz/
Opening 'https://stash.mycompany.com/projects/PROJ/repos/somestashrepo/browse/foo/bar/baz'...
```

```
nick@isis:~/dev/somestashrepo/foo/bar (master)$ git-browse baz.ext
Opening 'https://stash.mycompany.com/projects/PROJ/repos/somestashrepo/browse/foo/bar/baz.ext'...
```

If you need to link directly to a particular line number in a file, you can do that by using the `--line` argument:

```
nick@isis:~/dev/somestashrepo (master)$ git-browse foo/bar/baz.ext --line=25
Opening 'https://stash.mycompany.com/projects/PROJ/repos/somestashrepo/browse/foo/bar/baz.ext#25'...
```

```
nick@isis:~/dev/somegithubrepo (master)$ git-browse foo/bar/baz.ext --line=25
Opening 'https://github.com/someuser/somegithubrepo/blob/master/foo/bar/baz.ext#L25'...
```

### Head References
By default(*), the script will assume you want the link to correspond with the branch, tag, or commit (the "head") that you currently have checked out.  However, it's possible to pass in a different head reference by using the `--ref` argument to the script.  This argument will accept any branch, tag, or commit, and adjust the generated URL accordingly.
> (*) Automatic reference resolution is only possible with the use of the Git completion
> Bash script.  More information on this available below in the "Installation & Setup" section.

Open current path on the somebranch branch:

```
nick@isis:~/dev/somestashrepo (master)$ git-browse --ref=somebranch
Opening 'https://stash.mycompany.com/projects/PROJ/repos/somestashrepo/browse?at=somebranch'...
```

```
nick@isis:~/dev/somegithubrepo (master)$ git-browse --ref=somebranch
Opening 'https://github.com/someuser/somegithubrepo/tree/somebranch'...
```

Open current path at the 1.2.3 tag:

```
nick@isis:~/dev/somestashrepo (master)$ git-browse --ref=1.2.3
Opening 'https://stash.mycompany.com/projects/PROJ/repos/somestashrepo/browse?at=1.2.3'...
```

### Commit Listings
You may also have a need to view the current commit listing for a given head.  This is possible by passing the `--commits` flag:

```
nick@isis:~/dev/somestashrepo (master)$ git-browse --commits
Opening 'https://stash.mycompany.com/projects/PROJ/repos/somestashrepo/commits'...
```

```
nick@isis:~/dev/somegithubrepo (master)$ git-browse --commits
Opening 'https://github.com/someuser/somegithubrepo/commits/master'...
```

This flag can be used in combination with the `--ref` argument to show the listing for any branch or tag:

```
nick@isis:~/dev/somestashrepo (master)$ git-browse --commits --ref=somebranch
Opening 'https://stash.mycompany.com/projects/PROJ/repos/somestashrepo/commits?at=somebranch'...
```

```
nick@isis:~/dev/somestashrepo (master)$ git-browse --commits --ref=1.2.3
Opening 'https://stash.mycompany.com/projects/PROJ/repos/somestashrepo/commits?at=1.2.3'...
```

### Single Commit Details
`git-browse` also allows users to look up a single commit by passing in the commit hash instead of a file or directory:

```
nick@isis:~/dev/somestashrepo (master)$ git log -n1
commit 3ae1b55e6e32594143d75498a07a488ca7cd860f
Author: Some User <some.user@email.com>
Date:   Thu Apr 10 17:17:43 2014 +0000

    This is a commit message

nick@isis:~/dev/somestashrepo (master)$ git-browse 3ae1b55e6e32594143d75498a07a488ca7cd860f
Opening 'https://stash.mycompany.com/projects/PROJ/repos/somestashrepo/commits/3ae1b55e6e32594143d75498a07a488ca7cd860f'...
```

```
nick@isis:~/dev/somegithubrepo (master)$ git-browse 3ae1b55e6e32594143d75498a07a488ca7cd860f
Opening 'https://github.com/someuser/somegithubrepo/commit/3ae1b55e6e32594143d75498a07a488ca7cd860f'...
```

### Just Show Me The URL, Already!
If you only want to see the URL, but don't it automatically opened in your browser, simply pass the `--url-only` flag along with any combination of arguments already described:

```
nick@isis:~/dev/somestashrepo (master)$ git-browse foo/bar/baz.ext --ref=somebranch --line=25 --url-only
https://stash.mycompany.com/projects/PROJ/repos/somestashrepo/browse/foo/bar/baz.ext?at=somebranch#25
```

```
nick@isis:~/dev/somegithubrepo (master)$ git-browse foo/bar/baz.ext --ref=somebranch --line=25 --url-only
Opening 'https://github.com/someuser/somegithubrepo/blob/somebranch/foo/bar/baz.ext#L25'...
```

## Contributing
Please feel free to fork this repo and contribute to this script.  If contributing, please update the [unit tests](https://github.com/nickmoorman/git-browse/blob/test-git-browse.py) accordingly and make sure all tests pass.

## Changelog
v0.1.2 (2014-04-17) - Improved handling of Git completion script
v0.1.1 (2014-04-17) - Separated display logic from other logic
v0.1.0 (2014-04-11) - Initial Release
