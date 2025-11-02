"""
GitHub Utility

Adds a new chapter to the docs/chapters/ directory via the GitHub API.
Replace with your repo name and generate a personal access token for authentication.
"""
from github import Github

def add_chapter(repo_name, token, chapter_title, content_md):
    g = Github(token)
    repo = g.get_repo(repo_name)
    file_path = f"docs/chapters/{chapter_title.replace(' ', '_')}.md"
    repo.create_file(
        path=file_path,
        message=f"Add chapter: {chapter_title}",
        content=content_md,
        branch="main"
    )