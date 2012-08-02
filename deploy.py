from celery import chain
from export_svn import export_svn
from create_zip import create_zip
from upload_to_s3 import upload_to_s3
from deploy_to_beanstalk import create_application_version, update_environment


_chain = chain( export_svn.s() | create_zip.s() | upload_to_s3.s() | create_application_version.s() | update_environment.s() )

repo = ''
rev = '85'
zip_name = ''
bucket_name = ''
application_name = ''
version_label = ''
environment_name = ''
res = _chain(repo, rev, zip_name, bucket_name, application_name, version_label, environment_name)
