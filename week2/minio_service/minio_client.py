from config import ConfMinio
from minio import Minio
from minio.error import S3Error


def minio_auth(access=ConfMinio.access, secret=ConfMinio.secret):
    return Minio(
            'localhost:9000',
            access_key=access,
            secret_key=secret,
            secure=False
        )


class MinioCrud:
    minio = minio_auth()

    @staticmethod
    def create_new_bucket(bucket_name=ConfMinio.bucket_name, minio=minio):
        print(bucket_name)
        if not minio.bucket_exists(bucket_name):
            try:
                minio.make_bucket(bucket_name)
            except S3Error:
                raise

    @staticmethod
    def upload_object_to_bucket(file_name, path_to_file, bucket_name=ConfMinio.bucket_name, minio=minio):
        try:
            minio.fput_object(
                bucket_name,
                file_name,
                path_to_file
            )
        except S3Error:
            raise

    @staticmethod
    def delete_object(object_name, bucket_name=ConfMinio.bucket_name, minio=minio):

        try:
            minio.remove_object(
                bucket_name, object_name
            )
        except S3Error:
            raise

    @staticmethod
    def delete_bucket(bucket_name=ConfMinio.bucket_name, minio=minio):
        print(minio.list_objects(bucket_name))
        if minio.list_objects(bucket_name) is None:
            try:
                minio.remove_bucket(
                    bucket_name
                )
            except S3Error:
                raise
        else:
            for objects in minio.list_objects(bucket_name):
                minio.remove_object(bucket_name, objects.object_name)
            try:
                minio.remove_bucket(
                    bucket_name
                )
            except S3Error:
                raise

    @staticmethod
    def get_obj(obj_name, bucket_name=ConfMinio.bucket_name, minio=minio):
        return minio.get_object(
            bucket_name,
            obj_name)  # to decode u can use .data.decode()

    @staticmethod
    def download_obj(obj_name, patch_to_file, bucket_name=ConfMinio.bucket_name, minio=minio):
        return minio.fget_object(bucket_name, obj_name, patch_to_file+f'/{obj_name}')



