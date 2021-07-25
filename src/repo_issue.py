from dataclasses import dataclass
import datetime
from typing import List


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
