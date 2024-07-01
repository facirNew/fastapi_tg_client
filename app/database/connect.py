from typing import BinaryIO

from config import settings
from loguru import logger
from minio import Minio
from minio.commonconfig import Tags
from minio.lifecycleconfig import Expiration, Filter, LifecycleConfig, Rule
from mongoengine import connect
from telemongo import MongoSession


class MinIO:
    """
    MinIO settings
    """
    def __init__(self):
        print('try to create MinIO client')
        self.client = Minio(f'{settings.MINIO_SERVER_HOST}:{settings.MINIO_SERVER_PORT}',
                            access_key=settings.MINIO_ROOT_USER,
                            secret_key=settings.MINIO_ROOT_PASSWORD,
                            cert_check=False,
                            secure=False,
                            )
        logger.info('MinIO client create successful')

    def found_bucket(self, bucket_name: str = 'qrcode') -> None:
        """
        Get MinIO bucket or create it
        """
        logger.info('found MinIO bucket')
        found = self.client.bucket_exists(bucket_name)
        if not found:
            config = LifecycleConfig(
                [Rule(rule_filter=Filter(prefix=''),
                      status='Enabled',
                      expiration=Expiration(days=1))])
            self.client.make_bucket(bucket_name)
            logger.info('Created bucket', bucket_name)
            self.client.set_bucket_lifecycle(bucket_name, config)
            logger.info('Bucket configurated', bucket_name)

    def upload_file(self, file: BinaryIO, filename: str, bucket_name: str = 'qrcode') -> None:
        """
        Upload file to target bucket
        """
        self.found_bucket(bucket_name)
        tags = Tags(for_object=True)
        tags['type'] = 'image'
        self.client.put_object(
            bucket_name,
            object_name=filename,
            data=file,
            length=-1,
            part_size=5 * 1024 * 1024,
            tags=tags
        )

    def get_file_link(self, filename: str | None, bucket_name: str = 'qrcode') -> str | None:
        """
        Get link for download file
        """
        if filename is None:
            return None
        self.found_bucket(bucket_name)
        url = self.client.presigned_get_object(bucket_name, filename)
        return url


class MongoDB:
    def __init__(self):
        self.host = (f'mongodb://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@'
                     f'{settings.MONGO_HOST}:{settings.MONGO_PORT}/'
                     f'?retryWrites=true&w=majority')
        connect(db='telesession', host=self.host)
        self.session = MongoSession(database='telesession', host=self.host)


mongo_connection = MongoDB()
minio_connection = MinIO()
