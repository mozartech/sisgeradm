from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    bucket_name = 'sisadm-media'
    location = ''
    custom_domain = False
    default_acl = 'private'
    file_overwrite = True
    querystring_auth = True