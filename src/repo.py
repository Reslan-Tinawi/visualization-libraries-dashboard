from typing import List

from github import Github
import pandas as pd
from repo_issue import RepoIssue
from repo_pull_request import RepoPullRequest


class Repo:

    def __init__(self, name, token) -> None:
        self.name = name
        self.git = Github(token)
        self.__token = token
        self.repo = self.git.get_repo(self.name)

    def get_repo_features(self) -> list:
        """
        returns a list contains the main features of a repository
        featrues are : id, name, total_commits, total_stars, forks_count, created_at, contrib_count 
        """
        repo_id = self.repo.id
        repo_name = self.repo.name
        repo_language = self.repo.language
        total_commits = self.repo.get_commits().totalCount
        total_stars = self.repo.stargazers_count
        forks_count = self.repo.forks_count
        creation_date = self.repo.created_at
        contrib_count = self.repo.get_contributors().totalCount
        return [repo_id, repo_name, total_commits, total_stars, forks_count, creation_date, contrib_count]

    def get_contrib_features(self) -> pd.DataFrame:
        """
        returns a pandas dataframe contains the repo contributors and their features
        columns of the dataframe: repo_id, contrib_id, contrib_name, contrib_company, 
        contrib_location, contrib_repos_count
        """
        contributors = list(self.repo.get_contributors())
        contribs_features = [[self.repo.id, contrib.id, contrib.name,
                              contrib.company, contrib.location, contrib.get_repos().totalCount] \
                             for contrib in contributors]
        df = pd.DataFrame(contribs_features)
        df.columns = ['repo_id', 'contrib_id', 'contrib_name',
                      'contrib_company', 'contrib_location', 'contrib_repos_count']
        return df

    def get_repo_releases(self) -> pd.DataFrame:
        """
        returns a pandas dataframe contains info about repository releases
        columns are: repo_id, tag_name, created_at
        """
        releases = list(self.repo.get_releases())
        if len(releases) == 0:
            return pd.DataFrame()
        releases_features = [[self.repo.id, release.tag_name, release.created_at.strftime('%d-%m-%Y')]
                             for release in releases]
        df = pd.DataFrame(releases_features)
        df.columns = ['repo_id', 'tag_name', 'created_at']
        return df

    def get_repo_stars_history(self) -> pd.DataFrame:
        """
        returns a dataframe contains the stargazers history and their dates
        columns are: repo_id , starred_id
        """
        stars = list(self.repo.get_stargazers_with_dates())
        stars_features = [[self.repo.id, star.starred_at.strftime('%d-%m-%Y')] for star in stars]
        df = pd.DataFrame(stars_features)
        df.columns = ['repo_id', 'starred_at']
        return df

    def get_repo_issues(self) -> List[RepoIssue]:
        repo_issues: List[RepoIssue] = []

        for issue in self.repo.get_issues(state='all'):
            repo_issues.append(RepoIssue(
                id=issue.id,
                number=issue.number,
                repo_id=self.repo.id,
                created_at=issue.created_at,
                closed_at=issue.closed_at,
                state=issue.state,
                title=issue.title,
                body=issue.body,
                total_comments=issue.comments,
                labels=list(map(lambda label: label.name, issue.labels))
            ))

        return repo_issues

    def get_repo_pull_requests(self) -> List[RepoPullRequest]:
        repo_prs: List[RepoPullRequest] = []

        for repo_pr in self.repo.get_pulls(state='all'):
            repo_prs.append(RepoPullRequest(
                id=repo_pr.id,
                number=repo_pr.number,
                repo_id=self.repo.id,
                created_at=repo_pr.created_at,
                closed_at=repo_pr.closed_at,
                state=repo_pr.state,
                title=repo_pr.title,
                body=repo_pr.body,
                total_comments=repo_pr.comments,
                total_commits=repo_pr.commits,
                labels=list(map(lambda label: label.name, repo_pr.labels))
            ))

        return repo_prs
