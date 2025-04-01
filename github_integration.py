import os
from dotenv import load_dotenv
from github import Github
from github.GithubException import GithubException

# .env 파일에서 환경 변수 로드
load_dotenv()

class GitHubIntegration:
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError("GitHub 토큰이 설정되지 않았습니다. .env 파일에 GITHUB_TOKEN을 설정해주세요.")
        self.github = Github(self.token)

    def list_repositories(self, visibility="all"):
        """사용자의 GitHub 레포지토리 목록을 가져옵니다.
        
        Args:
            visibility (str): 'all', 'public', 'private' 중 하나
        
        Returns:
            list: 레포지토리 정보 목록
        """
        try:
            user = self.github.get_user()
            repos = []
            
            for repo in user.get_repos(visibility=visibility):
                repo_info = {
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "description": repo.description,
                    "url": repo.html_url,
                    "private": repo.private,
                    "created_at": repo.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": repo.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "language": repo.language,
                    "stars": repo.stargazers_count,
                    "forks": repo.forks_count
                }
                repos.append(repo_info)
            
            return repos
        except GithubException as e:
            print(f"레포지토리 목록 조회 중 오류 발생: {e}")
            return []

    def create_repository(self, name, description=None, private=False):
        """새로운 GitHub 저장소를 생성합니다."""
        try:
            user = self.github.get_user()
            repo = user.create_repo(
                name=name,
                description=description,
                private=private
            )
            return repo
        except GithubException as e:
            print(f"저장소 생성 중 오류 발생: {e}")
            return None

    def create_or_update_file(self, repo_name, file_path, content, commit_message):
        """파일을 생성하거나 업데이트합니다."""
        try:
            repo = self.github.get_user().get_repo(repo_name)
            try:
                # 기존 파일이 있는지 확인
                file = repo.get_contents(file_path)
                repo.update_file(
                    path=file_path,
                    message=commit_message,
                    content=content,
                    sha=file.sha
                )
            except:
                # 파일이 없으면 새로 생성
                repo.create_file(
                    path=file_path,
                    message=commit_message,
                    content=content
                )
            return True
        except GithubException as e:
            print(f"파일 생성/업데이트 중 오류 발생: {e}")
            return False

    def create_issue(self, repo_name, title, body=None):
        """이슈를 생성합니다."""
        try:
            repo = self.github.get_user().get_repo(repo_name)
            issue = repo.create_issue(title=title, body=body)
            return issue
        except GithubException as e:
            print(f"이슈 생성 중 오류 발생: {e}")
            return None

    def create_pull_request(self, repo_name, title, head, base="main", body=None):
        """풀 리퀘스트를 생성합니다."""
        try:
            repo = self.github.get_user().get_repo(repo_name)
            pr = repo.create_pull(
                title=title,
                body=body,
                head=head,
                base=base
            )
            return pr
        except GithubException as e:
            print(f"풀 리퀘스트 생성 중 오류 발생: {e}")
            return None 