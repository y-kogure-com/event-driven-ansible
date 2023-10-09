"""github_commit

Check Github repository's new commits

Arguments:
---------
    ** requires
    repository:
    token:

    ** optional
    base_url: defaults="https://api.github.com"
    branch: defaults="main"
    delay: delay seconds. defaults=5
"""

import asyncio
from typing import Any

import sys
import datetime
import inspect
from github import Github
from github import Auth

async def main(queue: asyncio.Queue, args: dict[str, Any]) -> None:
    if "repository" not in args:
        msg = 'Missing required argument: repository'
        raise ValueError(msg)
    elif "token" not in args:
        msg = 'Missing required argument: token'
        raise ValueError(msg)

    token = args.get('token')
    repository = args.get('repository')
    base_url = args.get('base_url', 'https://api.github.com')
    branch = args.get('main')
    delay = args.get('delay', 5)

    auth = Auth.Token(token)
    g = Github(base_url=base_url, auth=auth)

    try:
        repo_branch = g.get_user().get_repo(repository)
        commits = repo_branch.get_commits()
        dt_latest = datetime.datetime.strptime(commits[0].last_modified, '%a, %d %b %Y %H:%M:%S %Z') + datetime.timedelta(seconds=1)
    except:
        raise

    while True:
        try:
            commits = repo_branch.get_commits(since=dt_latest)
        except Exception:
            raise

        if commits.totalCount > 0:
            members = inspect.getmembers(commits[0], lambda m: type(m) is str)
            await queue.put({ k: v for k, v in members})
            dt_latest = datetime.datetime.strptime(commits[0].last_modified, '%a, %d %b %Y %H:%M:%S %Z') + datetime.timedelta(seconds=1)
        await asyncio.sleep(delay)

if __name__ == "__main__":
    """MockQueue if running directly."""

    class MockQueue:
        """A fake queue."""

        async def put(self: "MockQueue", event: dict) -> None:
            """Print the event."""
            print(event)

    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} <repository> <token>')
        exit()

    asyncio.run(
        main(
            MockQueue(),
            {
                "repository": sys.argv[1],
                "token": sys.argv[2],
            },
        ),
    )
