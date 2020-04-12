from google.cloud import storage
from urllib import request
import os
import logging
logging.basicConfig(level=logging.INFO)

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

def getbooks(request):
    if request.args and 'bucket' in request.args:
        bucket = request.args.get("bucket")
    if request.args and 'folder' in request.args:
        folder = request.args.get("folder")
    if request.args and 'query' in request.args:
        query = request.args.get("query")
	#set storage client

    downloadlocation = os.path.abspath(os.path.join("/tmp", "download"))
    from gutenberg import GetData
    GetData(query , refresh=False,downloadLocation=downloadlocation).GetBooks()

    logging.info(f"Uploading to Cloud Storage {bucket}/{folder} for query {query}")
    for f in os.listdir(downloadlocation):
        path  =  os.path.abspath(os.path.join(downloadlocation,f))
        upload_blob(bucket,path,f"{folder}/{f}")


if __name__ == "__main__":
    class Object(object):
        pass
    request = Object()
    request.args = {"bucket": "kbs_bookstore" , "folder" : "book_downloads" , "query" : "hinduism"}
    getbooks(request)
