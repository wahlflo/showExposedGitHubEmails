# showExposedGitHubEmails
Is a crawler which lists all email addresses used in commits of a specific GitHub user using the GitHub API.

It iterates through all public respositories owned by the user and all commits in each of these repositories.  


## Installation

Install the package with pip

    pip install exposed-github-user-emails-scanner

## Usage
Type ```showExposedGitHubEmails  --help``` to view the help.

```
usage: showExposedGitHubEmails [OPTION]... -u USERNAME

A crawler which lists all email addresses used in commits of a specific GitHub user using the GitHub API.

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  username of the user whose public repositories should be scanned
  -r REPOSITORY, --repository REPOSITORY
                        name of specific repository which should be scanned (default is all repositories)
  -t TOKEN, --token TOKEN
                        provide a GitHub token to increase the API quota which can be used by this script
  -v, --verbose         verbose mode
  -d DELAY, --delay DELAY
                        the delay between to requests in seconds (default is 1 second)
  --api-url API_URL     specify the URL to the GitHub Api (default is "https://api.github.com")
  --no-forks            ignore forked repositories

```

## Example
```
$ showExposedGitHubEmails -u AFictionalUsername
[+] Scan for public repositories of user AFictionalUsername
[+] Found 4 public repositories
[+] Scan repository my_first_project
[+] Scan repository project_2
[+] Exposed emails and names:
         41277220+aficionalusername@users.noreply.github.com - John Doe
         john.doe@hotmail.com                                - JD; John Doe
         john.doe@company.com                                - John Doe (Software Eng.)
```
