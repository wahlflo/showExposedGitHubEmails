import requests
import json
from collections import defaultdict, namedtuple
import time
import argparse
from cli_formatter.output_formatting import warning, error, info, set_verbosity_level, Color, colorize_string
from typing import List, Dict, Set


HEADER = {'Accept': 'application/vnd.github.v3+json'}
HEADER.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36'})


# Delay of one second between requests
DELAY = 1


API_URL = 'https://api.github.com'


Repository = namedtuple('Repository', ['name', 'is_fork'])


def update_header(update_dict: dict):
    """ updates the request header which will be send on each request to the github api """
    HEADER.update(update_dict)


def set_delay(delay: int):
    """ sets the delay between two requests to the github api"""
    global DELAY
    DELAY = delay


def set_api_url(api_url: str):
    """ sets the URL to the used github api"""
    global API_URL
    API_URL = api_url


def get_all_repositories_of_a_user(username: str) -> List[Repository]:
    repositories_seen = set()
    repositories = list()
    page_counter = 1
    while True:
        continue_loop = True

        url = '{}/users/{}/repos?per_page=100&page={}'.format(API_URL, username, page_counter)
        result_dict = __api_call(url=url)

        if 'message' in result_dict and 'API rate limit exceeded for ' in result_dict['message']:
            warning('API rate limit exceeded - not all repos where fetched')
            break

        for repository in result_dict:
            repo_name = repository['name']
            if repo_name in repositories_seen:
                continue_loop = False
                break
            else:
                repositories.append(Repository(name=repo_name, is_fork=repository['fork']))
                repositories_seen.add(repo_name)

        if continue_loop and len(result_dict) == 100:
            page_counter += 1
        else:
            break
    return repositories


def get_all_emails_of_a_user(username: str, repo_name: str) -> Dict[str, Set[str]]:
    emails_to_name = defaultdict(set)
    seen_commits = set()
    page_counter = 1
    commit_counter = 1

    while True:
        continue_loop = True
        url = '{}/repos/{}/{}/commits?per_page=100&page={}'.format(API_URL, username, repo_name, page_counter)
        result_dict = __api_call(url=url)

        if 'message' in result_dict:
            if result_dict['message'] == 'Git Repository is empty.':
                info('Git repository is empty', verbosity_level=5)
                continue

            if 'API rate limit exceeded for ' in result_dict['message']:
                warning('API rate limit exceeded - not all repos where fetched')
                return emails_to_name

        for commit_dict in result_dict:
            sha = commit_dict['sha']
            if sha in seen_commits:
                continue_loop = False
                break

            seen_commits.add(sha)
            info('scan commit {}'.format(commit_counter), verbosity_level=5)
            commit_counter += 1

            if commit_dict['author'] is None:
                continue
            user = commit_dict['author']['login']
            if user.lower() == username.lower():
                commit = commit_dict['commit']
                author_name = commit['author']['name']
                author_email = commit['author']['email']
                committer_name = commit['committer']['name']
                committer_email = commit['committer']['email']
                emails_to_name[author_email].add(author_name)
                emails_to_name[committer_email].add(committer_name)
        if continue_loop and len(result_dict) == 100:
            page_counter += 1
        else:
            break
    return emails_to_name


def __api_call(url) -> dict:
    time.sleep(DELAY)
    response = requests.get(url=url, headers=HEADER, timeout=10)
    return json.loads(response.text)


def main():
    parser = argparse.ArgumentParser(usage='lad [OPTION]... -u USERNAME', description='Lists information about the FILEs (the current directory by default) including Alternate Data Streams.')
    parser.add_argument('-u', '--user', dest="user", help="Username of the user which public repositories should be scanned", type=str)
    parser.add_argument('-r', '--repository', dest='repository', help="check only one specific repository", type=str)
    parser.add_argument('-t', '--token', dest='token', help="Paste a GitHub token her to increase the API quota", type=str)
    parser.add_argument('-v', '--verbose', dest="verbose", help="verbose mode", action='store_true', default=False)
    parser.add_argument('-d', '--delay', dest="delay", help="The delay between to requests in seconds", type=int, default=None)
    parser.add_argument('--api-url', dest="api_url", help='Specify the URL to the GitHub Api (default is "{}")'.format(API_URL), type=str, default=None)
    parser.add_argument('--no-forks', dest="no_forks", help='Ignore forked repositories', action='store_true', default=False)

    parsed_arguments = parser.parse_args()

    if parsed_arguments.user is None:
        warning('No username specified')
        parser.print_help()
        exit()

    if parsed_arguments.token is not None:
        update_header({'Authorization': 'token {}'.format(parsed_arguments.token)})

    if parsed_arguments.delay is not None:
        set_delay(delay=parsed_arguments.delay)

    if parsed_arguments.api_url is not None:
        set_api_url(api_url=parsed_arguments.api_url)

    if parsed_arguments.verbose:
        set_verbosity_level(level=5)

    if parsed_arguments.repository is not None:
        repos_to_scan = [parsed_arguments.repository]
    else:
        info('Scan for public repositories of user {}'.format(parsed_arguments.user))
        repos_to_scan_sorted = sorted(get_all_repositories_of_a_user(username=parsed_arguments.user), key=lambda x: x.is_fork)
        repos_to_scan = [x.name for x in repos_to_scan_sorted if (parsed_arguments.no_forks and not x.is_fork) or not parsed_arguments.no_forks]
        info('Found {} public repositories'.format(len(repos_to_scan)))

    emails_to_name = defaultdict(set)
    try:
        for repo in repos_to_scan:
            info('Scan repository {}'.format(repo))
            emails_to_name_new = get_all_emails_of_a_user(username=parsed_arguments.user, repo_name=repo)
            for email, names in emails_to_name_new.items():
                emails_to_name[email].update(names)
    except KeyboardInterrupt:
        warning('Keyboard interrupt. Stopped scanning.')

    if len(emails_to_name) > 0:
        max_width_email = max([len(x) for x in emails_to_name.keys()])
        info('Exposed emails and names:')
        for email, names in emails_to_name.items():
            names_string = ''
            for i, n in enumerate(names):
                names_string += colorize_string(n, Color.BLUE)
                if i < len(names) - 1:
                    names_string += '; '
            print('\t', colorize_string(email.ljust(max_width_email), Color.RED) + ' - ' + names_string)
    else:
        info('No emails found')


if __name__ == '__main__':
    main()
