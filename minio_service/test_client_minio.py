import pytest
from minio_client import *
import os


class ConfMinioTestData:
    access = 'testkey'
    secret = 'testsecret'
    bucket_name = 'testbucket'
    world = 'lox'
    file_name = 'test.txt'
    path_to_datafile = os.getcwd().replace('/minio_service', r'/Churn_Modelling.csv')


class TestCrudMinio:
    @pytest.fixture
    def connect(self, login=ConfMinioTestData.access, password=ConfMinioTestData.secret):
        return MinioInit.minio_auth(login, password)

    def test_create_bucket(self, connect, bucket_name=ConfMinioTestData.bucket_name):
        if not connect.bucket_exists(bucket_name):
            MinioCrud.create_new_bucket(bucket_name)
        else:
            MinioCrud.delete_bucket(bucket_name)
            MinioCrud.create_new_bucket(bucket_name)
        assert connect.bucket_exists(bucket_name)

    def test_add_object_to_bucket(self, connect, file_name=ConfMinioTestData.file_name,
                                  bucket_name=ConfMinioTestData.bucket_name):
        MinioCrud.upload_object_to_bucket(file_name, ConfMinioTestData.path_to_datafile, bucket_name)
        for files in connect.list_objects(bucket_name):
            assert 1 if files.object_name == file_name else 0

    def test_remove_file_from_bucket(self, connect, file_name=ConfMinioTestData.file_name,
                                     bucket_name=ConfMinioTestData.bucket_name):
        MinioCrud.delete_object(file_name, ConfMinioTestData.bucket_name)
        for files in connect.list_objects(bucket_name):
            assert 0 if files.object_name == file_name else 1

    def test_download_object_from_bucket(self, connect, file_name=ConfMinioTestData.file_name,
                                         bucket_name=ConfMinioTestData.bucket_name):
        MinioCrud.upload_object_to_bucket(file_name, ConfMinioTestData.path_to_datafile, bucket_name)
        MinioCrud.download_obj(file_name, os.getcwd(), bucket_name)
        if os.path.exists(file_name):
            os.remove(file_name)


retcode = pytest.main()
