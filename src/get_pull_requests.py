import datetime
from dataclasses import dataclass
from typing import List

from github.Repository import Repository


@dataclass
class RepoPullRequest:
    id: int
    number: int
    repo_id: int

    created_at: datetime.datetime
    closed_at: datetime.datetime
    state: str

    title: str
    body: str

    total_comments: int
    total_commits: int
    labels: List[str]


def get_repo_pull_requests(repo: Repository) -> List[RepoPullRequest]:
    repo_prs: List[RepoPullRequest] = []

    for repo_pr in repo.get_pulls(state='all'):
        repo_prs.append(RepoPullRequest(
            id=repo_pr.id,
            number=repo_pr.number,
            repo_id=repo.id,
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
