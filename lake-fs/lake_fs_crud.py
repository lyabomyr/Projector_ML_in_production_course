import lakefs_client
from lakefs_client import models
from lakefs_client.client import LakeFSClient

configuration = lakefs_client.Configuration()
configuration.username = 'AKIAIOSFODNN7EXAMPLE'
configuration.password = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
configuration.host = 'http://localhost:8000'
client = LakeFSClient(configuration)


def crete_repository():
    repo = models.RepositoryCreation(name='repo', storage_namespace='s3://storage',
                                     default_branch='main')
    client.repositories.create_repository(repo)

crete_repository()

