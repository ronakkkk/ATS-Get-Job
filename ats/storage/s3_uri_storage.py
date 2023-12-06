from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'


class PublicResumeStorage(S3Boto3Storage):
    location = 'resumes'
    default_acl = 'public-read'
    file_overwrite = True

class TrainingDataCSV(S3Boto3Storage):
    location = 'trainingdatajobscsv'
    default_acl = 'public-read'
    file_overwrite = True
