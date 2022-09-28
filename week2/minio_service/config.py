import os
class ConfMinio:
    access = 'testkey'
    secret = 'testsecret'
    bucket_name = 'mlbucket'
    path_to_datafile = os.getcwd().replace('/minio_service',r'/Churn_Modelling.csv')



class ConfMinioTestData:
    access = 'testkey'
    secret = 'testsecret'
    bucket_name = 'testbucket'
    world = 'lox'
    file_name = 'test.txt'
    path_to_datafile = os.getcwd().replace('/minio_service', r'/Churn_Modelling.csv')