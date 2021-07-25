from dataclasses import dataclass
import datetime
from typing import List

from github.Repository import Repository


@dataclass
class RepoIssue:
    id: int
    number: int
    repo_id: int

    created_at: datetime.datetime
    closed_at: datetime.datetime
    state: str

    title: str
    body: str

    total_comments: int
    labels: List[str]


def get_repo_issues(repo: Repository) -> List[RepoIssue]:
    repo_issues: List[RepoIssue] = []

    for issue in repo.get_issues(state='all'):
        repo_issues.append(RepoIssue(
            id=issue.id,
            number=issue.number,
            repo_id=repo.id,
            created_at=issue.created_at,
            closed_at=issue.closed_at,
            state=issue.state,
            title=issue.title,
            body=issue.body,
            total_comments=issue.comments,
            labels=list(map(lambda label: label.name, issue.labels))
        ))

    return repo_issues
