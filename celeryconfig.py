BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND = 'amqp'
CELERY_IMPORTS = ('export_svn', 'create_zip', 'upload_to_s3', 'deploy_to_beanstalk')
