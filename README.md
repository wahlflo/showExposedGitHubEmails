# showExposedGitHubEmails
A crawler who lists all emails used by one person in github using the GitHup API.

## Installation

Install the package with pip

    pip install exposed-github-user-emails-scanner

## Usage
Type ```showExposedGitHubEmails  --help``` to view the help.

```
usage: showExposedGitHubEmails [OPTION]... -u USERNAME

Lists information about the FILEs (the current directory by default) including Alternate Data Streams.

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  Username of the user which public repositories should be scanned
  -r REPOSITORY, --repository REPOSITORY
                        check only one specific repository
  -t TOKEN, --token TOKEN
                        Paste a GitHub token her to increase the API quota
  -v, --verbose         verbose mode
  -d DELAY, --delay DELAY
                        The delay between to requests in seconds
  --api-url API_URL     Specify the URL to the GitHub Api (default is "https://api.github.com")
  --no-forks            Ignore forked repositories
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
