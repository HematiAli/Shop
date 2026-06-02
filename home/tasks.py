from bucket import bucket
from celery import shared_task

"""
celery -A A worker -l INFO
"""
def get_all_bucket_objects():
    result = bucket.get_object()
    return result


@shared_task
def delete_object_task(key):
    bucket.delete_object(key)

@shared_task
def download_object_task(key):
    bucket.download_object(key)