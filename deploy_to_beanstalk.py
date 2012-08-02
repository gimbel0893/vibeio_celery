import celery
import ConfigParser
import os
from boto.beanstalk.beanstalk import Beanstalk


settings = ConfigParser.ConfigParser()
with open(os.sep.join((os.getcwd(), 'development.ini')), 'r') as config_file:
    settings.readfp(config_file)
AWS_ACCESS_KEY = settings.get('app:main', 'deployer.aws_access_key')
AWS_SECRET_KEY = settings.get('app:main', 'deployer.aws_secret_key')


@celery.task
def create_application_version(key_name, bucket_name, application_name, version_label):
    b = Beanstalk(aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

    res = b.create_application_version(
            application_name = application_name,
            version_label = version_label,
            s3_bucket = bucket_name,
            s3_key = key_name
        )

    return res.application_version.version_label

@celery.task
def update_environment(version_label, environment_name):
    b = Beanstalk(aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

    res = b.update_environment(
            environment_name = environment_name,
            version_label = version_label
        )

    return res
