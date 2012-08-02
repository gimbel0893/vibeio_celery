from celery import chain
import ConfigParser
import os
from export_svn import export_svn
from create_zip import create_zip
from upload_to_s3 import upload_to_s3
from deploy_to_beanstalk import create_application_version, update_environment


settings = ConfigParser.ConfigParser()
with open(os.sep.join((os.getcwd(), 'development.ini')), 'r') as config_file:
    settings.readfp(config_file)
repo = settings.get('app:main', 'deployer.repo_uri') + '/' + settings.get('app:main', 'deployer.repo_name')
rev = 95
version_label = 'rev' + str(rev)
zip_name = version_label + '.zip'
bucket_name = settings.get('app:main', 'deployer.bucket_name')
application_name = settings.get('app:main', 'deployer.application_name')
environment_name = settings.get('app:main', 'deployer.environment_name')

_chain = chain( export_svn.s(repo, rev) | create_zip.s(zip_name) | upload_to_s3.s(bucket_name) | create_application_version.s(bucket_name, application_name, version_label) | update_environment.s(environment_name) )

def run():
    res = _chain()
    return res
