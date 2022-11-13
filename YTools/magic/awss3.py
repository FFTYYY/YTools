'''这个模块帮助使用AWS S3存数据。'''
import boto3
import tempfile
import pickle

class AWSS3:
    def __init__(self, key_id, key_sec, region, bucket):
        self.s3 = boto3.client("s3" , region_name = region , aws_access_key_id = key_id , aws_secret_access_key = key_sec)
        self.bucket = bucket
    def set(self, data, tar_path):
        data = pickle.dumps(data)
        tar_path = str(tar_path).replace("\\"  , "/")
        try:
            with tempfile.TemporaryFile(mode = "wb+") as fil:
                fil.write(data)
                fil.seek(0,0) # 文件指针移动到开头
                self.s3.upload_fileobj(fil , self.bucket , tar_path)
        except Exception:
            return False
        return True

    def get(self, tar_path):
        tar_path = str(tar_path).replace("\\"  , "/")
        try:
            with tempfile.TemporaryFile(mode = "wb+") as fil:
                self.s3.download_fileobj(self.bucket , tar_path, fil)
                fil.seek(0,0) # 文件指针移动到开头
                data = fil.read()
                data = pickle.loads(data)
        except Exception:
            return None
        return data

