import os
from github import Github
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

class ForgeGitManager:
    def __init__(self):
        self.gh = Github(GITHUB_TOKEN) if GITHUB_TOKEN else None

    def get_repo_summary(self, repo_name: str):
        if not self.gh:
            return "Error: GITHUB_TOKEN not set."
        try:
            repo = self.gh.get_repo(repo_name)
            return {
                "name": repo.name,
                "description": repo.description,
                "stars": repo.stargazers_count,
                "last_update": repo.updated_at.isoformat()
            }
        except Exception as e:
            return f"Error fetching repo: {e}"

forge_git = ForgeGitManager()
