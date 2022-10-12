import os
import logging
import pytest
logging.getLogger()


@pytest.mark.dev_mode
def test_fork_repo(tests_client, tests_data):
    user = tests_client.user
    # check if forked repo exist
    assert len(
        [item for item in user.get_repos() if item.name == tests_data.repo_path]) == 0, "forked repo wrongly exist"
    forked_repo = tests_client.fork_repo()  # fork a repo
    assert forked_repo.name == tests_data.repo_name


def test_clone(tests_client, tests_data):
    forked_repo = tests_client.get_forked_repo()
    assert os.path.exists(tests_data.git_tests_resource) == False, F"{tests_data.git_tests_resource} directory is not empty"
    cloned_repo = tests_client.get_cloned_repo(forked_repo)
    working_dir = cloned_repo.working_dir
    # check that cloned was a successful
    assert working_dir == os.path.join(tests_data.git_tests_resource, tests_data.repo_name), 'clone failed'
    assert os.path.exists(os.path.join(tests_data.git_tests_resource, tests_data.repo_name)) is True, 'clone failed'


def test_branch_creation(tests_client, tests_data):
    forked_repo = tests_client.get_forked_repo()
    cloned_repo = tests_client.get_cloned_repo(forked_repo)
    branches_before = set(cloned_repo.branches)
    new_branch = cloned_repo.create_head(tests_data.branch_name)  # create a new branch
    branches_after = set(cloned_repo.branches)
    assert branches_after.difference(
        branches_before).pop().name == tests_data.branch_name, F"branch {tests_data.branch_name} missing"
    new_branch.checkout() # move to new branch
    assert cloned_repo.active_branch == new_branch


def test_create_new_file(tests_client, tests_data):
    forked_repo = tests_client.get_forked_repo()
    cloned_repo = tests_client.get_cloned_repo(forked_repo)
    new_branch = cloned_repo.create_head(tests_data.branch_name)
    new_branch.checkout() # move to new branch
    working_dir = cloned_repo.working_dir
    with open(F"{working_dir}{os.sep}{tests_data.file_name}", 'w') as file:
        file.write(tests_data.file_text)
    untracked_files = cloned_repo.untracked_files
    assert ''.join(untracked_files) == tests_data.file_name, "created file wrongly not tracked by git"


def test_edit_readme(tests_client, tests_data):
    forked_repo = tests_client.get_forked_repo()
    cloned_repo = tests_client.get_cloned_repo(forked_repo)
    new_branch = cloned_repo.create_head(tests_data.branch_name)
    new_branch.checkout() # move to new branch
    working_dir = cloned_repo.working_dir
    with open(F"{working_dir}{os.sep}README.txt", 'a') as file:
        file.write(tests_data.readme_text)
    # check if changes were added to the end of the file
    with open(F"{working_dir}{os.sep}README.txt", 'r') as file:
        last_line = file.readlines()[-1]
    assert tests_data.readme_text == last_line, F"text wasn't added at end of README.txt"
    # check diff between the index and the working tree
    assert tests_client.get_changes(cloned_repo) == ['README.txt'], 'no git tracking for modify in README.txt file'


def test_commit_changes(github_client, tests_client, tests_data):
    forked_repo = tests_client.get_forked_repo()
    cloned_repo = tests_client.get_cloned_repo(forked_repo)
    new_branch = cloned_repo.create_head(tests_data.branch_name)
    new_branch.checkout() # move to new branch
    working_dir = cloned_repo.working_dir
    with open(F"{working_dir}{os.sep}{tests_data.file_name}", 'w') as file:
        file.write(tests_data.file_text)
    untracked_files = cloned_repo.untracked_files
    assert ''.join(cloned_repo.untracked_files) == tests_data.file_name, "created file not tracked by git"
    with open(F"{working_dir}{os.sep}README.txt", 'a') as file:
        file.write(tests_data.readme_text)
    assert tests_client.get_changes(cloned_repo) == ['README.txt'], 'no git tracking for modify in README.txt file'
    cloned_repo.git.add(all=True) # adding all changes to stage
    stage_after_add = tests_client.get_stage(cloned_repo)  # check files in stage
    assert len(set(stage_after_add).difference({'README.txt', tests_data.file_name})) == 0, 'not all changes in stage'
    cloned_repo.index.commit(F"add a new file: {''.join(untracked_files)}, add text to README.txt file")
    assert len(tests_client.get_stage(cloned_repo)) == 0, 'after commit: changed files are still in stage'


def test_push_and_verify(tests_client, tests_data):
    forked_repo = tests_client.get_forked_repo()
    cloned_repo = tests_client.get_cloned_repo(forked_repo)
    new_branch = cloned_repo.create_head(tests_data.branch_name)
    new_branch.checkout() # move to new branch
    working_dir = cloned_repo.working_dir
    with open(F"{working_dir}{os.sep}{tests_data.file_name}", 'w') as file:
        file.write(tests_data.file_text)
    with open(F"{working_dir}{os.sep}README.txt", 'a') as file:
        file.write(tests_data.readme_text)
    cloned_repo.git.add(all=True) # adding all changes to stage
    cloned_repo.index.commit(F"creation of {tests_data.file_name} and text added to README.txt file")
    origin = cloned_repo.remote(name='origin')
    origin.push(refspec=F"{tests_data.branch_name}")
    # compare between the local branch and the remote branch
    # if no difference, it implies that all changes were pushed successfully
    assert not cloned_repo.git.diff(tests_data.branch_name,
                                    tests_data.remote_branch) is False, 'remote branch is differ than the local one'

