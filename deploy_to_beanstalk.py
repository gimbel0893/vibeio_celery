import celery
import ConfigParse
import os


settings = ConfigParse()
with open(os.sep.join(os.getcwd(), 'development.ini'), 'r') as config_file:
    settings.readfp(config_file)
AWS_ACCESS_KEY = settings.get('app:main', 'deployer.aws_access_key')
AWS_SECRET_KEY = settings.get('app:main', 'deployer.aws_secret_key')


@celerly.task
def create_application_version(application_name, version_label, bucket, key):
    b = Beanstalk(aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

    b.create_application_version(
            application_name = application_name,
            version_label = version_label,
            s3_bucket = bucket.name,
            s3_key = key.name
        )

    return version_label

@celerly.task
def update_environment(environment_name, version_label)
    b = Beanstalk(aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

    b.update_environment(
            environment_name = environment_name,
            version_label = version_label
        )

    return True
