import os
import lakefs_client
from lakefs_client import models
from lakefs_client.client import LakeFSClient


repository_name = 'repoml'
storage_namespace = 's3://storage'
default_name_branch = 'main'
branch_name = 'mlproduction'
new_branch_name = 'mlproductonweek2'
file_name= 'Churn_Modelling.csv'
path_to_datafile = os.getcwd().replace('/lake-fs', r'/Churn_Modelling.csv')

configuration = lakefs_client.Configuration()
configuration.username = 'testuser'
configuration.password = 'testpass'
configuration.host = 'http://localhost:8000'
client = LakeFSClient(configuration)


def crete_repository(repository = repository_name, storage_name=storage_namespace, default_branch = default_name_branch):
    repo = models.RepositoryCreation(name=repository, storage_namespace=storage_name,
                                     default_branch=default_branch)
    client.repositories.create_repository(repo)

crete_repository()

def get_list_branches(repository = repository_name):
    list_bran = client.branches.list_branches(repository).results
    return list_bran

def create_branch(created_branch_name=branch_name, destin_branch = default_name_branch, repository = repository_name):
    client.branches.create_branch(repository=repository,
                                  branch_creation=models.BranchCreation(name=created_branch_name, source=destin_branch))

def upload_file(name_file = file_name, patch_file = path_to_datafile, branch= branch_name,repository = repository_name):
    with open(name_file, 'rb') as f:
        client.objects.upload_object(repository=repository, branch=branch,
                                     path=patch_file, content=f)

def diffing_single_branch(repository = repository_name, branch= new_branch_name):
    dif_bran = client.branches.diff_branch(repository=repository, branch=branch).results
    return dif_bran

def commit_data(repository = repository_name, branch = branch_name):
    client.commits.commit(
        repository=repository,
        branch=branch,
        commit_creation=models.CommitCreation(message='Added a CSV file!', metadata={'using': 'python_api'}))


def merge_branch(branch_name1 =branch_name, branch_name_destination = new_branch_name,  repository = repository_name):
    client.refs.merge_into_branch(repository=repository, source_ref=branch_name1,
                                  destination_branch=branch_name_destination)



