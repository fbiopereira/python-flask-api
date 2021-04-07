import os
from git import Repo, TagReference


class GitHelpers:

    def __init__(self, environment):
        self.environment = environment

    def get_git_repo(self):
        git_path = os.path.dirname(os.path.abspath(__file__))
        if os.name != 'nt':
            git_path = git_path.replace("/app/helpers", "")
        else:
            git_path = git_path.replace("\\app\\helpers", "")
        repo = Repo(git_path)
        return repo

    def get_git_last_commit(self):
        return str(self.get_git_repo().head.commit)

    def get_git_last_tag(self):
        try:
            tag_ref = TagReference.list_items(self.get_git_repo())[0]
            if tag_ref.tag is not None:
                return str(tag_ref.tag)
            else:
                return 'n0.0.0'
        except Exception:
            return 'e0.0.0'

    def get_service_version(self):
        if self.environment != 'production':
            return self.get_git_last_commit()
        else:
            return self.get_git_last_tag()