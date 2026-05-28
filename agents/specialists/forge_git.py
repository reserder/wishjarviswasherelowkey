import os
from github import Github
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

class ForgeGitManager:
    def __init__(self):
        self.gh = Github(GITHUB_TOKEN) if GITHUB_TOKEN else None

    def harvest_trending_tools(self, query: str = "topic:ai-agents", limit: int = 5):
        """Scans GitHub for top trending AI tools and architectural patterns."""
        if not self.gh: return "Error: GITHUB_TOKEN not set."
        try:
            repos = self.gh.search_repositories(query=query, sort="stars", order="desc")
            harvested = []
            for repo in repos[:limit]:
                harvested.append({
                    "full_name": repo.full_name,
                    "description": repo.description,
                    "url": repo.html_url,
                    "stars": repo.stargazers_count,
                    "readme": repo.get_readme().decoded_content.decode()[:2000] # Get snippet for analysis
                })
            return harvested
        except Exception as e:
            return f"Error harvesting repos: {e}"

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
