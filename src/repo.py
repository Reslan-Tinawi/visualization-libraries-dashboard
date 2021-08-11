from typing import List

from github import Github
import pandas as pd
from github.Repository import Repository

from repo_issue import RepoIssue
from repo_pull_request import RepoPullRequest


class Repo:
    def __init__(self, name: str, full_name: str, gh_client: Github):
        self.name = name
        self.full_name = full_name
        self.repo: Repository = gh_client.get_repo(self.full_name)

    def get_repo_features(self) -> pd.DataFrame:
        """
        returns a list contains the main features of a repository
        features are : id, name, total_commits, total_stars, forks_count, created_at, contrib_count
        """
        repo_id = self.repo.id
        repo_name = self.repo.name
        total_commits = self.repo.get_commits().totalCount
        total_stars = self.repo.stargazers_count
        total_forks = self.repo.forks_count
        creation_date = self.repo.created_at
        total_contributors = self.repo.get_contributors().totalCount

        return pd.DataFrame(
            data=[
                [
                    repo_id,
                    repo_name,
                    total_commits,
                    total_stars,
                    total_forks,
                    creation_date,
                    total_contributors,
                ]
            ],
            columns=[
                "repo_id",
                "repo_name",
                "total_commits",
                "total_stars",
                "total_forks",
                "creation_date",
                "total_contributors",
            ],
        )

    def get_contrib_features(self) -> pd.DataFrame:
        """
        returns a pandas dataframe contains the repo contributors and their features
        columns of the dataframe: repo_id, contrib_id, contrib_name, contrib_company,
        contrib_location, contrib_repos_count
        """
        contributors = list(self.repo.get_contributors())

        contributor_features = [
            [
                self.repo.id,
                contrib.id,
                contrib.name,
                contrib.company,
                contrib.location,
                contrib.get_repos().totalCount,
            ]
            for contrib in contributors
        ]

        df = pd.DataFrame(
            data=contributor_features,
            columns=[
                "repo_id",
                "contrib_id",
                "contrib_name",
                "contrib_company",
                "contrib_location",
                "contrib_repos_count",
            ],
        )
        return df

    def get_repo_releases(self) -> pd.DataFrame:
        """
        returns a pandas dataframe contains info about repository releases
        columns are: repo_id, tag_name, created_at
        """
        releases = list(self.repo.get_releases())

        if len(releases) == 0:
            return pd.DataFrame()

        releases_features = [
            [self.repo.id, release.tag_name, release.created_at.strftime("%d-%m-%Y")]
            for release in releases
        ]

        df = pd.DataFrame(
            data=releases_features, columns=["repo_id", "tag_name", "created_at"]
        )

        return df

    def get_stars_history(self) -> pd.DataFrame:
        """
        returns a dataframe contains the stargazers history and their dates
        columns are: repo_id , starred_id
        """
        stars = list(self.repo.get_stargazers_with_dates())

        stars_features = [
            [self.repo.id, star.starred_at.strftime("%d-%m-%Y")] for star in stars
        ]

        df = pd.DataFrame(data=stars_features, columns=["repo_id", "starred_at"])

        return df

    def get_repo_issues(self) -> pd.DataFrame:
        repo_issues: List[RepoIssue] = []

        for issue in self.repo.get_issues(state="all"):
            repo_issues.append(
                RepoIssue(
                    id=issue.id,
                    number=issue.number,
                    repo_id=self.repo.id,
                    created_at=issue.created_at,
                    closed_at=issue.closed_at,
                    state=issue.state,
                    title=issue.title,
                    body=issue.body,
                    total_comments=issue.comments,
                    labels=list(map(lambda label: label.name, issue.labels)),
                )
            )

        return pd.DataFrame(repo_issues)

    def get_repo_pull_requests(self) -> pd.DataFrame:
        repo_prs: List[RepoPullRequest] = []

        for repo_pr in self.repo.get_pulls(state="all"):
            repo_prs.append(
                RepoPullRequest(
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
                    labels=list(map(lambda label: label.name, repo_pr.labels)),
                )
            )

        return pd.DataFrame(repo_prs)
