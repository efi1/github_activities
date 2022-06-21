import logging
import os
import stat
from git import Repo, InvalidGitRepositoryError

logging.getLogger()


class TestsClient(object):
    def __init__(self, github_client, tests_data):
        self.org_name = tests_data.org_name
        self.github_client = github_client
        self.repo_name = tests_data.repo_name
        self.target_folder = tests_data.target_folder
        self.user = self.github_client.get_user()

    def is_repo_exist(self, repo_name=None):
        try:
            self.user.get_repo(repo_name if repo_name else self.repo_name)
            return True
        except Exception as e:
            logging.info(F"cannot find {self.repo_name} repo, Error: {e}")
            return False

    def fork_repo(self):
        self.delete_repo()  # delete forked repo if exist
        logging.info('forked repo deleted')
        org = self.github_client.get_organization(self.org_name)
        org_repo = org.get_repo(self.repo_name)
        self.user.create_fork(org_repo)
        logging.info(F"forked repo {self.repo_name} was created")
        forked_repo = self.user.get_repo(self.repo_name)
        assert forked_repo.fork is True
        return forked_repo

    def get_forked_repo(self):
        # check if forked repo exist in your github account
        if self.is_repo_exist():
            repo = self.user.get_repo(self.repo_name)
            logging.info(F"forked repo {self.repo_name} already exist")
        else:
            # create if not exist
            repo = self.fork_repo()
        return repo

    def get_cloned_repo(self, forked_repo):
        self.clear_clone()  # clone exist in tests_data.target_folder
        logging.info('local cloned repo deleted successfully')
        clone_url = forked_repo.clone_url
        os.makedirs(self.target_folder)
        try:
            Repo(self.target_folder)
        except InvalidGitRepositoryError:
            logging.info('before repo init - no repository yet')
        cloned_repo = Repo.clone_from(clone_url, os.path.join(self.target_folder, self.repo_name))
        return cloned_repo

    def delete_repo(self):
        if self.is_repo_exist():
            repo = self.user.get_repo(self.repo_name)
            repo.delete()
            logging.info(F"repo {self.repo_name} was deleted")
        assert self.is_repo_exist() is False, F"repo {self.repo_name} wrongly exist"

    def clear_clone(self, target_folder=None):
        target_folder = target_folder if target_folder else self.target_folder
        logging.info(F"deleting local repository in path {target_folder}")
        if os.path.exists(target_folder):
            for root, dirs, files in os.walk(target_folder, topdown=False):
                for name in files:
                    filename = os.path.join(root, name)
                    os.chmod(filename, stat.S_IWUSR)
                    os.remove(filename)
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(target_folder)
        assert os.path.exists(target_folder) == False


    @classmethod
    def get_stage(cls, cloned_repo):
        return [item.a_path for item in cloned_repo.index.diff(cloned_repo.head.commit)]

    @classmethod
    def get_changes(cls, cloned_repo):
        return [item.a_path for item in cloned_repo.index.diff(None)]


    def tear_down(self):
        logging.info('in tearDown...')
        self.delete_repo()
        self.clear_clone()
        # self.clear_htm_file()



