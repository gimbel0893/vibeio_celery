import celery
import ConfigParser
import os
import shutil
from boto.s3.connection import S3Connection
from boto.s3.bucket import Bucket
from boto.s3.key import Key


settings = ConfigParser.ConfigParser()
with open(os.sep.join((os.getcwd(), 'development.ini')), 'r') as config_file:
    settings.readfp(config_file)
AWS_ACCESS_KEY = settings.get('app:main', 'deployer.aws_access_key')
AWS_SECRET_KEY = settings.get('app:main', 'deployer.aws_secret_key')


@celery.task()
def upload_to_s3(zip_file, bucket_name):
    s3 = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)

    bucket = Bucket(s3, bucket_name)

    k = Key(bucket)
    k.key = os.path.basename(zip_file)
    k.set_contents_from_filename(zip_file)

    shutil.rmtree(os.path.dirname(zip_file))

    return k.name
