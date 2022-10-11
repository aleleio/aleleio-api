from datetime import datetime


def mock_startup_users(db):
    pass

def mock_get_latest_commit(repo):
    return datetime.utcnow()

def mock_get_repo():
    return MockRepo()

def mock_get_github_token():
    return "gh1234"

def mock_get_latest_sha():
    return "1234567"

def mock_set_latest_sha(sha=None):
    pass

class MockRepo:
    class Blob:
        def __init__(self):
            self.sha = '12345abc'

    def create_git_blob(self, content, encoding):
        return self.Blob()

    class InputTreeGitElement:
        pass

    class Commit:
        def __init__(self):
            self.sha = '12345abc'

    class Branch:
        def __init__(self, ref):
            self.ref = ref

        @property
        def commit(self):
            return MockRepo.Commit()

    def get_branch(self, ref):
        return self.Branch(ref)

    @staticmethod
    def get_git_tree(sha):
        return 'base_tree'

    @staticmethod
    def create_git_tree(element_list, base_tree):
        return 'tree'

    @staticmethod
    def get_git_commit(sha):
        return 'parent'

    def create_git_commit(self, message, tree, parents):
        return self.Commit()

    class Reference:
        @staticmethod
        def edit(sha):
            return 'branch_refs'

    def get_git_ref(self, path):
        return self.Reference


