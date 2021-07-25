import datetime
from dataclasses import dataclass
from typing import List


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
